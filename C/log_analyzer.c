#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <string.h>
#define QUEUE_SIZE 10

int total_lines = 0;
int info_count = 0;
int warning_count = 0;
int error_count = 0;
int producer_done = 0;


pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t buffer_not_full = PTHREAD_COND_INITIALIZER;
pthread_cond_t buffer_not_empty = PTHREAD_COND_INITIALIZER;


struct Message_queue{
    
    char buffer[QUEUE_SIZE][1024];
    int head;
    int tail;
    int count;
};

struct Message_queue queue;

void *producer(void *arg){

  
    char line[1024];
    
    FILE *file = fopen((char *)arg, "r");
    if (file == NULL) {
        perror("Failed to open log file");
        pthread_mutex_lock(&mutex);
        return NULL;
    }

   while(fgets(line, sizeof(line), file)){
    pthread_mutex_lock(&mutex);

   while(queue.count == QUEUE_SIZE){

    pthread_cond_wait(&buffer_not_full, &mutex);
}
    line[strcspn(line, "\n")] = 0;
    
    strncpy(queue.buffer[queue.tail], line, sizeof(queue.buffer[queue.tail]) - 1);

    queue.tail = (queue.tail + 1) % QUEUE_SIZE;
    queue.count++;
    total_lines++;
    pthread_cond_signal(&buffer_not_empty);
    pthread_mutex_unlock(&mutex);

   }
   pthread_mutex_lock(&mutex);
   producer_done = 1;
   pthread_cond_broadcast(&buffer_not_empty);
   pthread_mutex_unlock(&mutex);
    fclose(file);
    return NULL;

}

void *consumer(void *arg){
    (void)arg;
    while(1){
        pthread_mutex_lock(&mutex);

        while(queue.count == 0 && !producer_done){
        pthread_cond_wait(&buffer_not_empty, &mutex);
        }

    
        if (queue.count == 0 && producer_done) {
            pthread_mutex_unlock(&mutex);
            return NULL;
        }

        char line[1024];
        strcpy(line, queue.buffer[queue.head]);
    

        queue.head = (queue.head + 1) % QUEUE_SIZE;
        queue.count--;

   
        pthread_cond_signal(&buffer_not_full);
        pthread_mutex_unlock(&mutex);

    

        if (strstr(line, "INFO") != NULL){
            pthread_mutex_lock(&mutex);
            info_count++;
            pthread_mutex_unlock(&mutex);
        }
        else if (strstr(line, "WARNING") != NULL){
            pthread_mutex_lock(&mutex);
            warning_count++;
            pthread_mutex_unlock(&mutex);
        }
        else if (strstr(line, "ERROR") != NULL){
            pthread_mutex_lock(&mutex);
            error_count++;
            pthread_mutex_unlock(&mutex);
        }

    }   
   
    return NULL;
}

int main(int argc, char *argv[]){
    if (argc != 3) {
        printf("Usage: <log_file>, number of threads\n");
        return 1;
    }


    const char *log_file = argv[1];
    int num_threads = atoi(argv[2]);
    queue.head = 0;
    queue.tail = 0;
    queue.count = 0;

    if(num_threads <= 0){
        fprintf(stderr, "Number of threads must be greater than 0\n");
        return 1;
    }


    pthread_t producer_thread, consumer_thread[num_threads];
    

    if (pthread_create(&producer_thread, NULL, producer, (void *)log_file) != 0) {

        printf("Failed to create producer thread\n");

        return 1;
    }

    for(int i =0; i < num_threads; i++){

        if(pthread_create(&consumer_thread[i], NULL, consumer, NULL) != 0){

            printf("Failed to create consumer thread\n");

            return 1;
        }
    }
    pthread_join(producer_thread, NULL);

    for(int i =0; i < num_threads; i++){

        pthread_join(consumer_thread[i], NULL);

    }
    
    printf("Total lines: %d\n", total_lines);
    printf("INFO: %d\n", info_count);
    printf("WARNING: %d\n", warning_count);
    printf("ERROR: %d\n", error_count);


    return 0;

}