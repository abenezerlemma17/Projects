//Abenezer Lemma
import java.util.Scanner;
public class CarpetCalculator {
    static Scanner sc = new Scanner(System.in);

/* To start with I made Scanner earlier in advance so made it static Scanner so I dont have to add a scanner in each method,
I catagorized according to the output, I made rooms first then the price, was able to get input validation after forever,
then finally the number of carpet needed
    */

    public static int[] room(){
        System.out.print("Enter room number: ");
        int room_number = sc.nextInt();
        while(room_number < 1) {
                System.out.println("Invalid room number ");
                System.out.print("Please enter a valid room number:  ");
                room_number = sc.nextInt();

        }
// the one above is the input validation for num rooms and the one bellow is iterating over size room
        //I was a bit unsure on how to reiterate and did it through trial and error
       int [] size_room = new int [room_number];

       for(int i = 0; i < room_number; i++){
           System.out.print("Enter square feet for room " + (i+1) + ": ");
           size_room[i] = sc.nextInt();

          if(size_room[i] < 150){
               System.out.println("Invalid room size");
               System.out.print("Please enter a valid room size:  ");
           }

       }

    return size_room;
    }

    public static double total_price(int rools, double price_input) {
// this was my longest one that i spent time on till i relaised that there is no need for any type of loops becuase i was assuming everything was in main and java still
        // a bit new
        double total_price_per_roll;
        int hours_per_roll = 6;
        int price_per_hour = 30;
        int total_labor;
        int hours_needed;
        double carpet_price = 0;
        double total_cost;
// math was pretty confusing till I changed the names then it worked
        //but soo many variable
            total_price_per_roll = rools * price_input;
            carpet_price += total_price_per_roll;

            hours_needed = rools * hours_per_roll;
            total_labor = hours_needed * price_per_hour;

           total_cost = total_labor + carpet_price;


        System.out.println("Carpet price: " +carpet_price);
        System.out.println("Labor Charges: " + total_labor);
        System.out.println("TOTAL COST: " + total_cost);

        return carpet_price;

    }

    public static int total_carpet(int [] size){
        int square_per_carpet = 150;
        int hours_per_roll = 6;
        double totalArea = 0;
// the forloop i will be honest was a complete guess but it worked so I am not complaing
        //however I made sure i understood it, that is that the int j goes and displays every index at size depending on how many
        // square feet per rooms, it then takes the value of each index of j and adds it to the total area until there are no more
        // indexes, if i were to print total area in the loop, it would show me every single iteration but i decided to put it outside
        for (int j : size) {
            totalArea += j;
        }
        //tried removing the int but keeps shouting at me, so happy IDE happy life.
        int rools = (int) (totalArea/square_per_carpet);
        int hours = hours_per_roll * rools;

        System.out.println("Total area is: " + totalArea);
        System.out.println("Total rolls carpet needed is: " + rools);
        System.out.println("Hours of labour needed is: " + hours);

        return rools;
    }

    public static void main(String[] args) {
        System.out.println("Program 4");
        System.out.println();
        int[] Rooms = room();
//I decided to put the input validation of price here because at first it was at the function but everytime it ran it would ask for the price after displayed
        // so after an hour so I thought of it as python but the input validation in main
        // I was a bit mad and happy at the same time
        System.out.print("Enter the price per roll: ");
        double price_input = sc.nextDouble();

        while (price_input < 50) {
            System.out.print("Please enter a valid price for per roll: ");
            price_input = sc.nextDouble();
        }

        System.out.println();
        System.out.println("====Carpet Instalilation Summary====");
        System.out.println();
        int Carpet = total_carpet(Rooms);
        total_price(Carpet,price_input);




    }
}
