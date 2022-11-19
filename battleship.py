
import helper
from helper import WATER, SHIP, HIT_WATER, HIT_SHIP  # 0,1,2,3
from helper import SHIP_SIZES, NUM_ROWS, NUM_COLUMNS, get_input

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "01233456789"


def init_board(rows, columns):
    return [[WATER for i in range(columns)] for j in range(rows)]


def cell_locations(board):
    return {(i, j) for i in range(len(board)) for j in range(len(board[0]))}


def cell_loc(loc):  # A2
    str_loc = "".join(loc)
    lis = []
    if loc[0] in LETTERS:
        lis.append(int(str_loc[1:]) - 1)
        lis.append(ord(str_loc[0]) - 65)
    else:
        return
    return tuple(lis)


def needed_locations(loc, size):
    return [(loc[0] + i, loc[1]) for i in range(size)]


def updated_cell_locations(board, size):
    res = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == WATER:
                valid = valid_ship(board, size, (i, j))
                if valid:
                    res.add((i, j))

    # print("Valid shit locations for computer: \n", res)
    return res


def valid_computer_hit(board):
    res = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == WATER:
                res.add((i, j))
    # print("valid conputer hit locationsL]: \n", res)
    return res


def turn_upper(string):
    lis = list(string)
    for i in range(len(lis)):
        if lis[i] not in NUMBERS:
            lis[i] = lis[i].upper()
    "".join(lis)
    return lis


def valid_ship(board, size, loc):
    valid = True
    locations = needed_locations((loc[0], loc[1]), size)
    for location in locations:
        if location in cell_locations(board):
            if board[location[0]][location[1]] != 1:
                continue
            else:
                valid = False
                return valid
        else:
            valid = False
            return valid
    return valid


def valid_input(inpt, board):
    lis_of_input = list(inpt)
    if " " in lis_of_input:
        return False
    if len(lis_of_input) > 3 or len(lis_of_input) < 2:
        return False
    for item in lis_of_input[1:]:
        if item not in NUMBERS:
            return False
    if helper.is_int(lis_of_input[0]):
        return False

    cell_location = cell_loc(turn_upper(inpt))
    if cell_location:
        if cell_location in cell_locations(board):
            pass
        else:
            return False
    return True


def create_player_board(rows, columns, ship_sizes):
    board = init_board(rows, columns)
    for ship in ship_sizes:
        helper.print_board(board)
        valid = False
        while not valid:
            ship_input = helper.get_input(
                f"Enter top coordinate for ship of size {ship}: ")
            if valid_input(ship_input, board):
                upper_version = turn_upper(ship_input)
                needed_loc = cell_loc(upper_version)
                is_valid_ship = valid_ship(board, ship, needed_loc)
                if is_valid_ship:
                    valid = True
                else:
                    print("Ship accident, many caualties, try again")
                    helper.print_board(board)
            else:
                print("Bruh that's some bad input")
                helper.print_board(board)

        for loc in needed_locations(needed_loc, ship):
            board[loc[0]][loc[1]] = SHIP
    return board


def fire_torpedo(board, loc):
    board_attribute = board[loc[0]][loc[1]]
    if loc not in cell_locations(board):
        return board
    else:
        if board_attribute == WATER:
            board[loc[0]][loc[1]] = HIT_WATER
        if board_attribute == SHIP:
            board[loc[0]][loc[1]] = HIT_SHIP
    return board


def create_computer_board(rows, cols, ships):
    board = init_board(rows, cols)
    for ship in ships:
        loc = helper.choose_ship_location(board, ship,
                                          updated_cell_locations(board, ship))
        for i in needed_locations(loc, ship):
            board[i[0]][i[1]] = SHIP
    return board


def play():
    human_board = create_player_board(NUM_ROWS,
                                      NUM_COLUMNS,
                                      SHIP_SIZES)
    computer_board = create_computer_board(NUM_ROWS,
                                           NUM_COLUMNS,
                                           SHIP_SIZES)
    human_hit_count = 0
    computer_hit_count = 0
    return human_board, computer_board, human_hit_count, computer_hit_count


def play_again(winner):
    user_input = get_input(f"{winner} wins! Do you wish to play again?")
    if user_input in "YN" and len(user_input)!=0:
        if user_input == "Y":
            return True
        else:
            return False
    else:
        while True:
            user_input_ = get_input("please insert Y or N ONLY.")
            if user_input_ in "YN" and len(user_input_) != 0:
                if user_input_ == "Y":
                    return True
                elif user_input_ == "N":
                    return False


def hidden_board(board):
    hidden = []
    cur = []
    for pos, row in enumerate(board):
        for pos1, item in enumerate(row):
            if item == SHIP:
                cur.append(WATER)
            else:
                cur.append(board[pos][pos1])
        hidden.append(cur)
        cur = []

    return hidden


def main():
    human_board, computer_board, human_hit_count, computer_hit_count = play()
    game = True
    helper.print_board(human_board, hidden_board(computer_board))
    while game:
        while human_hit_count != sum(SHIP_SIZES) or computer_hit_count != sum(
                SHIP_SIZES):
            hit = False
            while not hit:
                human_hit_request = get_input(
                    "Please enter a valid bombing location: ")
                if valid_input(turn_upper(human_hit_request), computer_board):
                    cell_bombing_location = cell_loc(
                        turn_upper(human_hit_request))
                    if computer_board[cell_bombing_location[0]][
                        cell_bombing_location[1]] != HIT_SHIP and \
                            computer_board[cell_bombing_location[0]][
                                cell_bombing_location[1]] != HIT_WATER:
                        fire_torpedo(computer_board, cell_bombing_location)
                        hit = True
                        if computer_board[cell_bombing_location[0]][
                            cell_bombing_location[1]] == HIT_SHIP:
                            human_hit_count += 1

                    else:
                        print("Did you understand how to win? maybe\\"
                              " try hitting ships ")
                else:
                    print("Invalid input!")
            computer_hit = helper.choose_torpedo_target(
                hidden_board(human_board),
                valid_computer_hit(hidden_board(human_board)))
            if human_board[computer_hit[0]][computer_hit[1]] == SHIP:
                computer_hit_count += 1
                human_board[computer_hit[0]][computer_hit[1]] = HIT_SHIP

            elif human_board[computer_hit[0]][computer_hit[1]] == WATER:
                human_board[computer_hit[0]][computer_hit[1]] = HIT_WATER

            if computer_hit_count == sum(
                    SHIP_SIZES) or human_hit_count == sum(
                SHIP_SIZES):
                helper.print_board(human_board, computer_board)

                if computer_hit_count == sum(
                        SHIP_SIZES) and human_hit_count == sum(SHIP_SIZES):
                    winner = "Both human and computer"
                elif computer_hit_count == sum(SHIP_SIZES):
                    winner = "Computer"
                else:
                    winner = "Human"
                if play_again(winner):
                    human_board, computer_board, human_hit_count, \
                    computer_hit_count = play()
                else:
                    return

            helper.print_board(human_board, hidden_board(computer_board))


if __name__ == "__main__":
    main()
