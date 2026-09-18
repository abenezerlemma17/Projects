#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <sys/types.h>
#include <stdlib.h>
#include <sys/wait.h>

int main (int argc,char *argv[])
{
    if (argc != 2){
        printf("Either display A or B");
        return 1;
    }
    char *FIFO_PATH_1 = "/tmp/chat_ab";
    char *FIFO_PATH_2 = "/tmp/chat_ba";

    if (mkfifo(FIFO_PATH_1, 0666) == -1) {
        if (errno != EEXIST){
        perror("mkfifo");
        exit(EXIT_FAILURE);
    }
        
    }

   
    if (mkfifo(FIFO_PATH_2, 0666) == -1) {
        if (errno != EEXIST){
        perror("mkfifo");
        exit(EXIT_FAILURE);}
        
    }
    
    int fd_read;
    int fd_write;
    pid_t pid;
    char end[] = "exit\n";
    

    char num1[] = "A";
    char num2[] = "B";

    char arr[30];

    if (strcmp(argv[1], num1) == 0){
        
        printf("CHAT START role=%s pid=%d\n", num1, getpid());

        fflush(stdout);

        fd_read = open(FIFO_PATH_2, O_RDONLY);

        fd_write = open(FIFO_PATH_1, O_WRONLY);

        pid = fork();

        if (pid < 0){
            perror("pid");
            close(fd_read);
            close(fd_write);
            return 2;
        }

        if (pid == 0){

            close(fd_write);

        while(1){
            
            ssize_t msg = read(fd_read, arr, sizeof(arr)-1);

            if(msg < 0){
                perror("read");
                close(fd_read);
                exit(1);
            }
            else if(msg == 0){
                break;
            }
                
                write(STDOUT_FILENO, "Peer: ", 6);
                write(STDOUT_FILENO, arr, msg);
                arr[msg] = '\0';
                if (strcmp(arr, end) == 0){
                    break;
                }
        }
        }

        else {

         close(fd_read);


            while(1){
            fgets(arr, sizeof(arr), stdin);
            size_t len = strlen(arr);
            write(fd_write, arr, len);

            if (strcmp(arr, end) == 0){
                break;
            }
            }
        }
        close(fd_write);
         wait(NULL);
       
    }

    if (strcmp(argv[1], num2) == 0){
        
        printf("CHAT START role=%s pid=%d\n", num2, getpid());

        fflush(stdout);
        
        
        fd_read = open(FIFO_PATH_1, O_RDWR);

       
        fd_write = open(FIFO_PATH_2, O_WRONLY);
        pid = fork();

        if (pid < 0){
            perror("pid");
            close(fd_read);
            close(fd_write);
            return 2;
        }

        if (pid == 0){
            close(fd_write);

        while(1){
            
            ssize_t msg = read(fd_read, arr, sizeof(arr) - 1);

            if(msg < 0){
                perror("read");
                close(fd_read);
                exit(1);
            }
            else if(msg == 0){
                break;
            }
                
                write(STDOUT_FILENO, "Peer: ", 6);
                write(STDOUT_FILENO, arr, msg);
                arr[msg] = '\0';
                if (strcmp(arr, end) == 0){
                    break;
                }
                
        }
        close(fd_read);
         exit(0);
        }

        else{

        close(fd_read);

        while(1){

            fgets(arr, sizeof(arr), stdin);
            size_t len = strlen(arr);
            write(fd_write, arr, len);

            if (strcmp(arr, end) == 0){
                break;
            }
        }
        }
        close(fd_write);
        wait(NULL);
    }
    if(strcmp(argv[1], "A")==0){
    unlink(FIFO_PATH_1);
    unlink(FIFO_PATH_2);
    }
    return 0;
}
