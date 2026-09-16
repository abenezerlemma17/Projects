//Abenezer Lemma
import java.util.*;
public class Flashcards {
    static Scanner sc = new Scanner(System.in);

    // --- Data model ---
    static class Flashcard {
        private final String question;
        private final String answer;

        Flashcard(String question, String answer) {
            this.question = question;
            this.answer = answer;
        }

        public String getQuestion() {
            return question;
        }

        public String getAnswer() {
            return answer;
        }

        /**
         * Case-insensitive, trims user input.
         */
        public boolean isCorrect(String userInput) {
            if (userInput == null) return false;
            return answer.trim().equalsIgnoreCase(userInput.trim());
        }

        @Override
        public String toString() {
            return "Q: " + question + "  |  A: " + answer;
        }

    }

    // --- Seed data: a few trivia cards ---
    private static ArrayList seedCards() {
        // Feel free to change these or add more!
        ArrayList cards = new ArrayList<>();
        cards.add(new Flashcard("What planet is known as the Red Planet?", "Mars"));
        cards.add(new Flashcard("In which year did the Titanic sink?", "1912"));
        cards.add(new Flashcard("What is the chemical symbol for gold?", "Au"));
        cards.add(new Flashcard("Who painted the Mona Lisa?", "Leonardo da Vinci"));
        cards.add(new Flashcard("What is the largest ocean on Earth?", "Pacific"));
        cards.add(new Flashcard("How many continents are there?", "7"));
        Collections.shuffle(cards);//I choose to shuffle them earlier so that they would be shuffled at first.
        return cards;
    }

    public static void main(String[] args) {
        System.out.println("=====Flashcard Quizzer=====");
        System.out.println();
        int num_ques;
        String answer;
        String new_question;
        String new_answer;
// As I did in previous programs, I always create the variable beforehand so its easier to give them a value
        ArrayList<Flashcard> deck = seedCards();
//I chose the putting the program in the main because it would be easier for me to control every single input
        boolean run_again = true;
        int choice;
        while (run_again) {
            System.out.println("1) Take a quiz");
            System.out.println("2) Add a flashcard");
            System.out.println("3) list all the flashcard");
            System.out.println("4) Quit");
            System.out.print("Chose: ");

            choice = sc.nextInt();
            System.out.println();

            if (choice == 1) {
                System.out.print("How many sets of questions ");
                num_ques = sc.nextInt();

                while(num_ques > deck.size()) {
                    System.out.println("Invalid input. Please try again");
                    System.out.print("How many sets of questions ");
                    num_ques = sc.nextInt();
                }

                // here I put a input validation for the program above

                int score = 0;
                sc.nextLine();
                Collections.shuffle(deck);
                // I used sc.nectLine() to clear the buffer between num_ques and the answer also chose to make the score variable
                // outside the loop so that everytime the user ran the quiz again, the score would restart to zero
                // I shuffled the deck again before because I noticed that when it ran it would shuffle the first time but wouldnt do it again
                // so I made an educated guess and put it first inside the for loop and the outised the for loop but inside the while and if statement
                for (int i = 0; i < num_ques; i++) {
                    Flashcard card = deck.get(i);
                    System.out.println(card.getQuestion());
                    System.out.println();

                    System.out.print("Your answer is: ");
                    answer = sc.nextLine();

                    while (answer.trim().isEmpty()){
                        System.out.println("Invalid input. Please try again");
                        System.out.print("Your answer is: ");
                        answer = sc.nextLine();
                    }

                    if (card.isCorrect(answer)) {// I ended up using the isCorrect since it would have been easier to follow and understand
                        score += 1;
                        System.out.print("Correct! " + score + "/" + num_ques + "\n");

                    } else {
                        System.out.print("Wrong!" + " The correct answer is " + card.getAnswer() + "\n" + score + "/" + num_ques + "\n");
                    }
                }
                double percentage = Math.ceil(((double) score / (double) num_ques) * 100);
                System.out.println("Grade is " + percentage);
                System.out.println();
            } else if (choice == 2) {
                sc.nextLine();//same thing here this sc.nextLine is clearing any buffer between the user choice an the question and answer
                System.out.println("Enter the question you wish to add");
                new_question = sc.nextLine();

                System.out.println();

                System.out.println("Enter its answer");
                new_answer = sc.nextLine();

                if (new_question.trim().isEmpty() || new_answer.trim().isEmpty()) {
                    while (new_question.trim().isEmpty() || new_answer.trim().isEmpty()) {
                //I made  the input validation for the second choice so that when the user entered and empty space
                        //it would return invalid
                        System.out.println("Invalid input");
                        System.out.println("Enter the question you wish to add");
                        new_question = sc.nextLine();

                        System.out.println();

                        System.out.println("Enter its answer");
                        new_answer = sc.nextLine();

                    }
                }

            System.out.println();
            deck.add(new Flashcard(new_question, new_answer));
            System.out.println("Added successfully!");
            System.out.println();

        }
             else if (choice == 3) {//I was going to use a normal for loop but this one made more sense
            for (Flashcard card : deck) {
                System.out.println(card);
            }
            System.out.println();
        }

        if (choice == 4) {
            run_again = false;
            System.out.println("Thank you for using this program.");
        } else if (choice < 1 || choice > 4) {
            System.out.println("Invalid choice");
        }

    }

    }
}