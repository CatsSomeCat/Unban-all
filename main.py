try:
    import customtkinter, discord, requests, os, ctypes, colorama
    from discord.ext import commands
    from tkinter import messagebox
    from colorama import Fore
except ImportError as imerror:
    print(f"Module {imerror.name} not found, Try py -3 -m pip install -r requirements.txt to install all required module")

ctypes.windll.kernel32.SetConsoleTitleW("Unban all")
intents = discord.Intents.all()
client = commands.Bot(Intents=intents)
style = colorama.Style.NORMAL
colorama.init(convert=True, autoreset=True)
Blue = Fore.BLUE ; Green = Fore.GREEN ; Magenta = Fore.MAGENTA ; Gray = Fore.LIGHTBLACK_EX
Red = Fore.RED ; White = Fore.WHITE ; Cyan = Fore.CYAN ; Yellow = Fore.YELLOW ; Ocean = Fore.LIGHTCYAN_EX

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('%dx%d+%d+%d' % (350, 220, (self.winfo_screenwidth() / 2) - (350 / 2), (self.winfo_screenheight() / 2) - (420 / 2)))
        self.protocol("WM_DELETE_WINDOW", exit)
        self.resizable(False, False)
        self.title("Unban all")
        self.iconbitmap(os.path.join(os.path.dirname(__file__), "assets\icon.ico"), default=None)

        customtkinter.set_appearance_mode("dark")

        self.TKINTER_WIDGETS = {}
        self.token = None
        self.guild = None

        self.frame = customtkinter.CTkFrame(master=self, corner_radius=15)
        self.frame.grid(row=1, column=0, padx=21, pady=20)

        # Label Token
        self.TKINTER_WIDGETS['label_token'] = customtkinter.CTkLabel(master=self.frame, text="Token", width=30,
                                                                     height=25, corner_radius=10)
        self.TKINTER_WIDGETS['label_token'].grid(row=0, column=0, padx=10, pady=20)

        # Entry Token
        self.TKINTER_WIDGETS['entry_token'] = customtkinter.CTkEntry(master=self.frame,
                                                                     placeholder_text="Token", width=200,
                                                                     height=30, border_width=2, corner_radius=10,
                                                                     show="•")
        self.TKINTER_WIDGETS['entry_token'].grid(row=0, column=1, padx=10, columnspan=2)

        # Label Guild
        self.TKINTER_WIDGETS['label_guild'] = customtkinter.CTkLabel(master=self.frame, text="Guild ID ", width=30,
                                                                     height=25, corner_radius=10)
        self.TKINTER_WIDGETS['label_guild'].grid(row=1, column=0, padx=10, pady=5, sticky='e')

        # Entry Guild
        self.TKINTER_WIDGETS['entry_guild'] = customtkinter.CTkEntry(master=self.frame,
                                                                     placeholder_text="Guild ID", width=200,
                                                                     height=30, border_width=2, corner_radius=10)
        self.TKINTER_WIDGETS['entry_guild'].grid(row=1, column=1, padx=10, columnspan=2, pady=20)

        # Button Start
        self.TKINTER_WIDGETS['button_start'] = customtkinter.CTkButton(master=self.frame, text="Start", width=80,
                                                                       fg_color="#36719F", hover_color="#3B8ED0",
                                                                       text_color="#FFF", command=self.Start)
        self.TKINTER_WIDGETS['button_start'].grid(row=2, column=1, padx=0, pady=(0, 15), ipadx=10, ipady=0,
                                                  sticky='e')

        # Button Close
        self.TKINTER_WIDGETS['button_close'] = customtkinter.CTkButton(master=self.frame, text="Close",
                                                                       fg_color="#f54242",
                                                                       hover_color="#ff5252", text_color="#fff",
                                                                       width=80,
                                                                       command=exit)
        self.TKINTER_WIDGETS['button_close'].grid(row=2, column=2, padx=10, pady=(0, 15), sticky='e')

    def Checking(self):
        self.token, self.guild = self.TKINTER_WIDGETS['entry_token'].get(), self.TKINTER_WIDGETS['entry_guild'].get()
        if self.token.isspace() or not self.token:
            messagebox.showwarning("WARNING", "Enter the required values")
            return False
        elif not self.guild.isdigit() or not self.guild:
            messagebox.showwarning("WARNING", "Enter the required values")
            return False
        headers = {"Authorization": f"Bot {self.token}"}
        login = requests.get('https://discordapp.com/api/v9/auth/login', headers=headers, timeout=20)
        if login.status_code != 200:
            messagebox.showerror("ERROR", "Invalid Token")
            return False
        return True

    def Start(self):
        try:
            assert app.Checking() == True
            @client.event
            async def on_ready():
                print(Green + f"Online! client logged in as {client.user.name + client.user.discriminator}")
                try:
                    async for ban_entry in client.get_guild(int(self.guild)).bans():
                        await client.get_guild(int(self.guild)).unban(ban_entry.user)
                        print(Yellow + f"{ban_entry.user.name}#{ban_entry.user.discriminator} ID : {ban_entry.user.id} Unbanned Successfully")
                    print(Green + "Finished!"), self.destroy()
                except Exception as error:
                    print(Red + f"{error.__cause__}")
            client.run(self.token)
        except AssertionError:
            return False

if __name__ == "__main__":
    app = App()
    app.mainloop()