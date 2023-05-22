import discord
import dotenv
import os


def initialize():
    env_file_path = ".env"
    env_variables_list = ["DISCORD_BOT_TOKEN", "TEST", "BOT_TOKEN"]

    if not os.path.isfile(env_file_path):
        print("<?> .env not found. Creating new .env file with necessary variables.")
        with open(env_file_path, "w") as env_file:
            for variable_string in env_variables_list:
                env_file.write(variable_string + "=\n")
    else:
        with open(env_file_path, "r") as env_file:
            var_rows = env_file.readlines()

        with open(env_file_path, "w") as env_file:
            env_file_lines = []
            for var_row in var_rows:
                var_row_name = var_row.split("=")[0].strip()
                if var_row_name in env_variables_list:
                    env_file_lines.append(var_row)
                else:
                    print(f"<?> Removing {var_row_name} from .env")
            for variable_string in env_variables_list:
                if variable_string not in env_file_lines:
                    print(f"<?> Adding variable {variable_string} to .env")
                    env_file_lines.append(variable_string + "=\n")
            env_file.writelines(env_file_lines)


initialize()
