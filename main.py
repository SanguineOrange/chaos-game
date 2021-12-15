# Cameron Colliver for MSU Denver MTH3710 - Chaos and Nonlinear Dynamics
import matplotlib.pyplot
from random import randint


def main():
    print("Welcome!")
    print("This application simulates the chaos game given an amount of points and their location")
    # User prompt for number of points
    # Must be greater than 2 and valid integer otherwise prompt repeats
    while True:
        print("To start, please enter the number of points (must be greater than 2)")

        invalid_num: bool = True
        while invalid_num:
            num_points = input("Enter number: ")
            try:
                num_points = int(num_points)
                if num_points > 2:
                    break
                else:
                    print("Invalid number of points, make sure there are more than 2!")
            except ValueError:
                print("Error! Please enter an integer.")

        # Run the point generator to generate the boundary
        points_index = point_generator(num_points)
        print(points_index[0][1])

        print("\nTime to set restrictions")
        # Prompt user for if they want previous point to be valid
        no_previous = False
        while True:
            response = input("Are jumps to the previous point still allowed? (y/n): ")
            if response == "y" or response == "Y":
                no_previous = False
                break
            elif response == "n" or response == "N":
                no_previous = True
                break
            else:
                print("Error! I did not understand that. Please make sure your response is 'y' or 'n'")

        while True:
            # Prompt user if boundary centerpoint is valid
            response = input("Are jumps to the center allowed? (y/n): ")
            if response == "y" or response == "Y":
                # If it is it appends the centerpoint to the array of points
                points_index.append(find_centerpoint(points_index))
                break
            elif response == "n" or response == "N":
                break
            else:
                print("Error! I did not understand that. Please make sure your response is 'y' or 'n'")

        # Prompt user to enter jump ratio
        print("Please enter the jump length, "
              "this is the value that determines how far each jump goes relative to the destination point")
        while True:
            ratio = input("Enter the jump length: ")
            try:
                ratio = float(ratio)
                break
            except ValueError:
                print("Error! Please enter a number.")

        print("Simulating chaos game...")
        chaos_in_motion(num_points, points_index, no_previous, ratio)

        # If user wants to run another simulation, let them
        # Otherwise exit the program
        while True:
            response = input("Would you like to run another simulation? (y/n): ")
            if response == "y" or response == "Y":
                break
            elif response == "n" or response == "N":
                print("Thank you for using the chaos game simulator! Exiting...")
                return
            else:
                print("Error! I did not understand that. Please make sure your response is 'y' or 'n'")


# For the amount of points the user specified, create a 2d array with user defined boundary points
def point_generator(num_points):
    point_array = []
    print("Generating a chaos game using " + str(num_points) + " points")
    for i in range(0, int(num_points)):
        invalid_x: bool = True
        invalid_y: bool = True
        while invalid_x:
            x_coord = input("Please enter the value of the x coordinate: ")
            invalid_x = invalid_check(x_coord)
        while invalid_y:
            y_coord = input("Please enter the value of the y coordinate: ")
            invalid_y = invalid_check(y_coord)

        point_array.append([float(x_coord), float(y_coord)])
        print(point_array)
    return point_array


def invalid_check(number):
    try:
        float(number)
        return False
    except ValueError:
        print("Error! " + number + " is invalid, please try again")
        return True


# Function to find the centerpoint, used if midpoint is acceptable target
def find_centerpoint(point_array):
    x_coords = []
    y_coords = []
    for i in range(len(point_array)):
        x_coords.append(point_array[i][0])
        y_coords.append(point_array[i][1])
    # Returns the average of all coordinates x and y values
    return [(sum(x_coords) / len(point_array)), (sum(y_coords) / len(point_array))]


# Function to simulate the game
def chaos_in_motion(num_points, points_index, restrictive_no_previous: bool
                    , jump_ratio: float):
    # Iterations is hard coded to 250,000 but can be modified here
    iterations = 250000

    # Indexes for visited coordinates
    # Split into two since its a little easier than 2d arrays
    visited_x = [points_index[0][0], points_index[0][0]]
    visited_y = [points_index[0][0], points_index[0][0]]
    previous_target = -1  # previous target initializes as -1 since there is no previous target

    # For each iteration
    for i in range(1, iterations):
        # Pick a random point
        chaos_target = randint(0, len(points_index) - 1)
        # If the game is restrictive and we've been there already pick another
        if restrictive_no_previous:
            while chaos_target == previous_target:
                chaos_target = randint(0, int(num_points) - 1)
            previous_target = chaos_target
        # Find the sum of both points multiplied by r and store them in the visited points
        visited_x.append(jump_ratio * (visited_x[i] + points_index[chaos_target][0]))
        visited_y.append(jump_ratio * (visited_y[i] + points_index[chaos_target][1]))

    # Print the results
    matplotlib.pyplot.scatter(visited_x, visited_y, s=1)
    for point in points_index:
        matplotlib.pyplot.scatter(point[0], point[1], s=40)
    matplotlib.pyplot.show()


main()