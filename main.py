import discord
import dotenv
import os


def initialize():
    env_file_path = ".env"
    env_variables_list = ["BOT_TOKEN", ""]

    if not os.path.isfile(env_file_path):
        print("<?> .env not found. Creating new .env file")
        with open(env_file_path, "w") as env_file:
            for variable_string in env_variables_list:
                env_file.write(variable_string + "=\n")
    else:
        with open(env_file_path, "a+") as env_file:
            existing_variable_list = []
            for existing_variable in env_file:
                existing_variable_list.append(existing_variable.replace("=", ""))
            for variable_string in env_variables_list:
                if variable_string not in existing_variable_list:
                    env_file.write(variable_string + "=\n")

