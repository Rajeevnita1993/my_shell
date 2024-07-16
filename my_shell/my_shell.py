import subprocess
import os
import signal
import sys
import readline

# Global variable to store previous_directory
previous_directory = os.getcwd()
history_file = os.path.join(os.path.expanduser("~"), ".rksh_history")

def handle_cd_command(user_input):
    global previous_directory

    try:
        command_args = user_input.split()

        if len(command_args) == 1:
            new_directory = os.path.expanduser("~")
            os.chdir(os.path.expanduser("~"))
        elif command_args[1] == "-":
            if previous_directory:
                new_directory = previous_directory
            else:
                print("No previous directory")
                return
        else:
            new_directory = command_args[1]

        # Store current directory before changing to the new one
        current_directory = os.getcwd()
        os.chdir(new_directory)
        previous_directory = current_directory

        
    except Exception as e:
        print(f"Error changing directory: {e}")

def handle_pwd_command():
    try:
        # Print the current working directory
        print(os.getcwd())
    except Exception as e:
        print(f"Error getting current directory: {e}")


def execute_command(command_args):
    try:
        result = subprocess.run(command_args, capture_output=True, text=True)

        if result.returncode == 0:
            print(result.stdout, end='')
        else:
            print(result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Command '{command_args[0]}' failed with error: {e}")

    except FileNotFoundError:
        print(f"Command '{command_args[0]}' not found.")

    except Exception as e:
        print(f"An error occured: {e}")

def signal_handler(sig, frame):
    print("\nrksh> ", end='', flush=True)

def save_history():
    readline.write_history_file(history_file)

def load_history():
    if os.path.exists(history_file):
        readline.read_history_file(history_file)

def create_shell():
    global previous_directory

    # Load history from file
    load_history()

    # Set custom signal handler for signint
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            user_input = input("rksh> ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                break

            if user_input.lower() == "history":
                for i in range(1, readline.get_current_history_length() + 1):
                    print(readline.get_history_item(i))
                continue

            # Save command to history
            readline.add_history(user_input)

            if user_input.startswith("cd"):
                handle_cd_command(user_input)
                continue

            elif user_input == "pwd":
                handle_pwd_command()
                continue

            # Check if command contains a pipe "|"
            if "|" in user_input:
                commands = user_input.split("|")

                processes = []

                for command in commands:
                    command = command.strip()
                    command_args = command.split()

                    if processes:
                        # Chain process by redirecting stdout of previous command to stdin of current command
                        process = subprocess.Popen(command_args, stdin=processes[-1].stdout, stdout=subprocess.PIPE, text=True)
                    else:
                        process = subprocess.Popen(command_args, stdout=subprocess.PIPE, text=True)

                    processes.append(process)

                # Wait for last process to finish and capture its output
                output, _ = processes[-1].communicate()

                # Print final output of the last command in the chain
                print(output, end='')

            else:
                command_args = user_input.split()
                execute_command(command_args)

        except subprocess.CalledProcessError as e:
            print(f"Command '{command_args[0]}' failed with error: {e}")

        except FileNotFoundError:
            print(f"Command '{command_args[0]}' not found.")

        except EOFError:
            break  # EOFError is caught to handle end-of-file (Ctrl+D) gracefully, exiting the shell.

        except KeyboardInterrupt:
            print()

        except Exception as e:
            print(f"An error occured: {e}")

    # Save history to the file when exiting the shell
    save_history()



def main():
    create_shell()

if __name__ == "__main__":
    main()