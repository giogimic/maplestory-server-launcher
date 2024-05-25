import os

import subprocess

import logging

import threading

import tkinter as tk

from tkinter import scrolledtext, StringVar, OptionMenu



logging.basicConfig(level=logging.DEBUG,

                    format='%(asctime)s [%(levelname)s] %(message)s',

                    datefmt='%Y-%m-%d %H:%M:%S')



MAX_MEMORY = "4G"

MIN_MEMORY = "2G"



class MapleServerControlPanel:

    def __init__(self, master):

        self.master = master

        master.title("MapleStory Private Server Control Panel")

        master.configure(bg="#333333")



        self.console = scrolledtext.ScrolledText(master, wrap=tk.WORD, bg="#222222", fg="white")

        self.console.pack(fill=tk.BOTH, expand=True)



        self.button_frame = tk.Frame(master, bg="#333333")

        self.button_frame.pack()



        self.available_jars = [file for file in os.listdir() if file.endswith(".jar")]

        self.server_var = StringVar(master)

        self.server_var.set(self.available_jars[0] if self.available_jars else "")



        self.server_dropdown = OptionMenu(self.button_frame, self.server_var, *self.available_jars)

        self.server_dropdown.pack(side=tk.LEFT, padx=5, pady=5)



        self.start_button = tk.Button(self.button_frame, text="Start Server", command=self.start_server, bg="#555555", fg="white")

        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)



        self.stop_button = tk.Button(self.button_frame, text="Stop Server", command=self.stop_server, bg="#555555", fg="white")

        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)



        self.status_button = tk.Button(self.button_frame, text="Check Status", command=self.check_status, bg="#555555", fg="white")

        self.status_button.pack(side=tk.LEFT, padx=5, pady=5)



    def start_server(self):

        jar_file = self.server_var.get()

        if not jar_file:

            logging.error("No .jar files selected.")

            return



        self.log_info("Starting MapleStory Private Server...")

        try:

            self.server_process = subprocess.Popen(["java", f"-Xmx{MAX_MEMORY}", f"-Xms{MIN_MEMORY}", "-jar", jar_file, "nogui"],

                                           stdout=subprocess.PIPE,

                                           stderr=subprocess.STDOUT,

                                           universal_newlines=True)

            threading.Thread(target=self.display_output, args=(self.server_process.stdout,), daemon=True).start()

        except FileNotFoundError:

            self.log_error("Server .jar file not found.")

        except Exception as e:

            self.log_error(f"Error: {str(e)}")



    def stop_server(self):

        if hasattr(self, 'server_process') and self.server_process.poll() is None:

            self.log_info("Stopping MapleStory Private Server...")

            self.server_process.terminate()

            self.log_info("Server stopped.")

        else:

            self.log_error("Server is not running.")



    def check_status(self):

        if hasattr(self, 'server_process') and self.server_process.poll() is None:

            self.log_info("Server is running.")

        else:

            self.log_info("Server is not running.")



    def display_output(self, stdout):

        for line in iter(stdout.readline, ''):

            self.console.insert(tk.END, line)

            self.console.see(tk.END)



    def log_info(self, message):

        self.console.insert(tk.END, message + "\n")

        self.console.see(tk.END)



    def log_error(self, message):

        self.console.insert(tk.END, "[ERROR] " + message + "\n")

        self.console.see(tk.END)



def main():

    root = tk.Tk()

    app = MapleServerControlPanel(root)

    root.mainloop()



if __name__ == "__main__":

    main()
