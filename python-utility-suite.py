import easygui as gui
from PyPDF2 import PdfReader, PdfWriter
import os,shutil,re,zipfile,random
import pandas as pd
from random import shuffle
# Function to validate password
def validate_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&~`^#\-_+=,.<>\{\}\[\]\\\/|:;"\']).{8,}$'
    return bool(re.match(pattern, password))
gui.msgbox("Welcome to Python Utility Suite", "Python Utility Suite", "Click here")
greetings = [
    "Your smart desktop assistant is ready to help.",
    "Let's simplify your workflow today.",
    "System online. Tasks standing by.",
    "Organize, process, and optimize — you're in control.",
    "Efficiency starts here. Ready when you are.",
    "Smart tools. Simple interface. Seamless results.",
    "Back to business — your suite is at your service.",
    "Productivity unlocked. What would you like to do?"
]
# Main loop for the utility suite
while True:
 choices = ("File management", "Working with PDF", "Working with OS","Compression", "Encryption and Decryption","Data Cleaning","CSV tool","Surprise Me","Exit")
 title = "Python Utility Suite"
 user_c =gui.choicebox(random.choice(greetings),"Python Utility Suite",choices)
 if user_c == "Exit":
        gui.msgbox("Thank you for using Python Utility Suite. Goodbye!", "Python Utility Suite")
        break
 # File management tasks
 while user_c == "File management":
    choices1 = ("Create", "Open", "Write", "Append", "Seek", "Back to Main Menu")
    file_task = gui.choicebox("Choose task:", title, choices1)

    if file_task == "Back to Main Menu":
        break

    if file_task == "Create":
        file_name = gui.enterbox("Enter the name of the file to create: ")
        if file_name:
            try:
                with open(file_name, "w") as file:
                    gui.msgbox(f"File {file_name} is created successfully.")
            except:
                gui.msgbox("Error")
    elif file_task == "Open":   
        file_name = gui.fileopenbox("Enter the name of the file to open:")
        if file_name:
            with open(file_name, "r") as file:
                content = file.read()
                gui.msgbox(content, title=f"Content of {file_name}")
    elif file_task == "Write":
        file_name = gui.fileopenbox("Enter the name of the file to write.")
        if file_name:
            with open(file_name, "w") as file:
                text_write = gui.enterbox(f"Enter your prompt to be put in {file_name}")
                file.write(text_write)
                gui.msgbox(f"Text is written into the file {file_name}")
    elif file_task == "Append":
        file_name = gui.fileopenbox("Enter the name of the file to append.")
        if file_name:
            with open(file_name, "a") as file:
                text_write = gui.enterbox(f"Enter your text to append into file:")
                file.write("\n" + text_write)
                gui.msgbox(f"Text is appended into the file {file_name}")
    elif file_task == "Seek":
 # Ask user for file path and position
        file_name = gui.fileopenbox("Select a file to seek in:")
        if file_name:
 # Ask user for the position they want to seek to
            position_type = gui.choicebox("Seek relative to:", choices=["Beginning", "Current position", "End"])
            seek_position = int(gui.enterbox("Enter the number of bytes to seek:"))
        try:
            with open(file_name, "r") as file:
 # Determine the seek position
                if position_type == "Beginning":
                    file.seek(seek_position, 0) # Seek from the beginning
                elif position_type == "Current position":
                    file.seek(seek_position, 1) # Seek from the current position
                elif position_type == "End":
                    file.seek(seek_position, 2) # Seek from the end
 # Read and show content from the new file position
                content = file.read()
                gui.msgbox(f"File content after seeking to position {seek_position} from {position_type}: \n\n{content}")
        except Exception as e:
            gui.exceptionbox(f"Error occurred during seek operation: {e}")
 # PDF-related tasks
 while user_c == "Working with PDF":
    choices2 = ("Merging", "Splitting", "Rotating", "Extracting pages", "Back to Main Menu")
    file_task = gui.choicebox("Choose task:", title, choices2)
    if file_task == "Back to Main Menu":
        break
    if file_task == "Merging":
        sr = gui.fileopenbox("Select the first PDF to merge")
        dst = gui.fileopenbox("Select the second PDF to merge")
        if sr and dst:
            pdf_files = [sr, dst]
            output_pdf = PdfWriter()
            for pdf_file in pdf_files:
                input_pdf = PdfReader(pdf_file)
                for page in input_pdf.pages:
                    output_pdf.add_page(page)
            output_file_path = gui.filesavebox("Save merged PDF as", default="merged.pdf")
            if output_file_path:
                with open(output_file_path, "wb") as output_file:
                    output_pdf.write(output_file)
                gui.msgbox(f"Merged PDF saved to:\n{output_file_path}", title)
        else:
            gui.msgbox("Merging cancelled. Both PDF files must be selected.", title)
    elif file_task == "Rotating":
        input_pdf_path = gui.fileopenbox("Select a PDF file to rotate")
        base_path = os.path.dirname(input_pdf_path)
        input_pdf = PdfReader(input_pdf_path)
        r = gui.enterbox("Enter the new file name: ")
        output_pdf_path = os.path.join(base_path, r)
        num_pages = int(gui.enterbox("Enter the number of pages you need to rotate"))

        output_pdf = PdfWriter()
        angle = int(gui.choicebox("Choose rotation angle:", choices=["90", "180", "270"]))

        for n in range(num_pages):
         page = input_pdf.pages[n]
         page.rotate(angle)
         output_pdf.add_page(page)

        with open(output_pdf_path, "wb") as x:
            output_pdf.write(x)
        gui.msgbox(f"Rotated PDF saved as:\n{output_pdf_path}", "Done")
    elif file_task == "Extracting pages":
        input_pdf_path = gui.fileopenbox("Select a PDF file to extract")
        base_path = os.path.dirname(input_pdf_path)
        input_pdf = PdfReader(input_pdf_path)
        f = gui.enterbox("Enter the New File Name : ")
        output_pdf_path = os.path.join(base_path, f)

        pages_to_extract = gui.enterbox("Enter the pages you want to extract")
        pages = [int(p.strip()) for p in pages_to_extract.split(',')]

        output_pdf = PdfWriter()
        for page_num in pages:
            page = input_pdf.pages[page_num - 1]
            output_pdf.add_page(page)
        with open(output_pdf_path, "wb") as output_file:
         output_pdf.write(output_file)

        gui.msgbox(f"Pages {pages_to_extract} have been extracted to {output_pdf_path}", "Done")
    elif file_task == "Splitting":
        input_pdf_path = gui.fileopenbox("Select a PDF file to split")
        base_path = os.path.dirname(input_pdf_path)
        f = gui.enterbox("Enter the New File Name : ")
        output_pdf_path = os.path.join(base_path, f)
        file = open(input_pdf_path, "rb")
        input_pdf = PdfReader(file)
        output_pdf = PdfWriter()

        for page_num in range(len(input_pdf.pages)):
            page_left = input_pdf.pages[page_num]
            page_right = input_pdf.pages[page_num]

            upper_right = page_left.mediabox.upper_right
            new_coords = (upper_right[0] / 2, upper_right[1])

            page_right.mediabox.upper_right = new_coords
            output_pdf.add_page(page_right)

            page_left.mediabox.upper_left = new_coords
            output_pdf.add_page(page_left)

        with open(output_pdf_path, "wb") as output_file:
            output_pdf.write(output_file)

        gui.msgbox(f"Split PDF saved as:\n{output_pdf_path}", "Done")
 # Encryption and Decryption tasks
 while user_c == "Encryption and Decryption":
    action = gui.choicebox("What would you like to do?", "PDF Encryption Tool", ["Encrypt PDF", "Decrypt PDF", "Back to Main Menu"])

    if action == "Back to Main Menu":
        break
    if action == "Encrypt PDF":
        input_path = gui.fileopenbox("Choose a PDF to encrypt", filetypes=["*.pdf"])
        if input_path:
            password = gui.passwordbox("Enter a password to encrypt the PDF:")
            if not password:
                gui.msgbox("No password entered. Exiting.")
            elif not validate_password(password):
                gui.msgbox("Password does not meet security criteria.\nIt must contain at least one lowercase, one uppercase, one digit, one special character, and be 8+ characters.")
            else:
                try:
                    with open(input_path, "rb") as infile:
                        reader = PdfReader(infile)
                        writer = PdfWriter()
                        for i in range(len(reader.pages)):
                            writer.add_page(reader.pages[i])
                        writer.encrypt(user_pwd=password, owner_pwd=None, use_128bit=True)
                    base_name = os.path.splitext(os.path.basename(input_path))[0]
                    output_path = gui.filesavebox("Save encrypted PDF as", default=f"{base_name}_encrypted.pdf")
                    if output_path:
                        with open(output_path, "wb") as outfile:
                            writer.write(outfile)
                        gui.msgbox(f"PDF encrypted successfully and saved to:\n{output_path}")
                except Exception as e:
                    gui.exceptionbox("An error occurred during encryption", str(e))
    elif action == "Decrypt PDF":
        input_path = gui.fileopenbox("Choose an encrypted PDF to decrypt", filetypes=["*.pdf"])
        if input_path:
            password = gui.passwordbox("Enter the password to decrypt the PDF:")
            if not password:
                gui.msgbox("No password entered. Exiting.")
        else:
            try:
                with open(input_path, "rb") as infile:
                    reader = PdfReader(infile)
                if reader.is_encrypted:
                    if not reader.decrypt(password):
                        gui.msgbox("Incorrect password. Could not decrypt.")
                    else:
                         writer = PdfWriter()
                         for i in range(len(reader.pages)):
                            writer.add_page(reader.pages[i])
                         output_path = gui.filesavebox("Save decrypted PDF as", default="decrypted.pdf")
                         if output_path:
                            with open(output_path, "wb") as outfile:
                                writer.write(outfile)
                            gui.msgbox(f"PDF decrypted successfully and saved to:\n{output_path}")
                else:
                    gui.msgbox("The selected PDF is not encrypted.")
            except Exception as e:
                gui.exceptionbox("An error occurred during decryption", str(e))

 # OS-related tasks
 while user_c == "Working with OS":
    choices3 = ("Listing", "Creating", "Rename", "Moving", "Backup", "Deleting", "Back to Main Menu")
    file_task = gui.choicebox("Choose task:", title, choices3)

    if file_task == "Back to Main Menu":
     break
    if file_task == "Listing":
        gui.msgbox(f"Current directory: {os.getcwd()}")
        file_list = "\n".join(os.listdir())
        
        gui.textbox("Files and Directories", "Directory Listing", file_list)
    elif file_task == "Creating":
        folder_name = gui.enterbox("Enter the name of the folder you want to create: ")
        if folder_name:
            os.mkdir(folder_name)
            gui.msgbox(f"Folder {folder_name} created successfully.")
    elif file_task == "Deleting":
        folder_name = gui.enterbox("Enter the name of the folder you want to delete: ")
        if folder_name:
            os.rmdir(folder_name)
            gui.msgbox(f"Folder {folder_name} deleted successfully.")
    elif file_task == "Rename":
        src = gui.enterbox("Enter the current name of the file/folder:")
        dest = gui.enterbox("Enter the new name:")
        try:
            os.rename(src, dest)
            gui.msgbox(f"Renamed '{src}' to '{dest}'.")
        except Exception as e:
            gui.exceptionbox(f"Error renaming: {e}")
    elif file_task == "Moving":
        src = gui.enterbox("Enter the name of the file/folder to move:")
        dest = gui.enterbox("Enter the destination path:")
        try:
            shutil.move(src, dest)
            gui.msgbox(f"Moved '{src}' to '{dest}'.")
        except Exception as e:
            gui.exceptionbox(f"Error moving file/folder: {e}")
    elif file_task == "Backup":
        src = gui.enterbox("Enter the folder name you want to back up:")
        dest = gui.enterbox("Enter the destination folder name for the backup:")
        try:
            shutil.copytree(src, dest)
            gui.msgbox(f"Backup completed: '{src}' → '{dest}'")
        except FileExistsError:
            gui.msgbox(f"Destination folder '{dest}' already exists. Choose a different name.")
        except FileNotFoundError:
            gui.msgbox(f"Source folder '{src}' not found.")
        except Exception as e:
            gui.exceptionbox(f"Error during backup: {e}")
 while user_c == "CSV tool":
    choices_csv = ("View Data","Drop Empty Rows","Fill Empty Cells","Display Specific Columns","Describe Data","Merge CSV Files","Split CSV by Row Count","Export Cleaned Data","Back to Main Menu"
)
    file_task = gui.choicebox("Choose task:", title, choices_csv)
    if file_task == "Back to Main Menu":
        break
    if file_task == "View Data":
        pd.options.display.max_rows = 99999
        path=gui.fileopenbox("Choose Csv file")
        df=pd.read_csv(path)
        gui.textbox("Csv Data Preview","CSV DATA",df.to_string())
    elif file_task == "Drop Empty Rows":
        path=gui.fileopenbox("Choose Csv file")
        df = pd.read_csv(path)
        new_df = df.dropna()
        gui.textbox("Cleaned Data Preview", "Cleaned CSV Data", df.to_string())
    elif file_task == "Fill Empty Cells":
    #replaceing the default value at empty places
        fill_value = gui.enterbox("Enter value to fill in empty cells:", default="N/A")
        df.fillna(fill_value, inplace=True)
        gui.textbox("Filled Data Preview", "Filled CSV Data", df.to_string())
    elif file_task == "Display Specific Columns":
    #print only speciefield columns
        path=gui.fileopenbox("Choose Csv file")
        df=pd.read_csv(path)
        col1=gui.enterbox("Enter first column which you want to display")
        col2=gui.enterbox("Enter second column which you want to display")
        
        gui.textbox("Specific Columns Preview", "CSV Data", df[[col1,col2]].to_string())

    elif file_task == "Export Cleaned Data":
        f=gui.enterbox("Enter New Csv file name to save the cleaned data ")
        output_path = gui.filesavebox("Save the cleaned CSV as:",f)
        if output_path:
            df.to_csv(output_path, index=False)
    elif file_task == "Describe Data":
        path=gui.fileopenbox("Choose Csv file")
        df = pd.read_csv(path)
        description = df.describe(include='all').to_string()
        gui.textbox("Descriptive Statistics", "Dataset Description", description)
    elif file_task == "Merge CSV Files":
        file1 = gui.fileopenbox("Select the first CSV file to merge")
        file2 = gui.fileopenbox("Select the second CSV file to merge")
        if file1 and file2:
            df1 = pd.read_csv(file1)
            df2 = pd.read_csv(file2)
            merged_df = pd.concat([df1, df2], ignore_index=True)
            gui.textbox("Merged CSV Preview", "Merged Data", merged_df.to_string())
 while user_c == "Compression":
    #compressing and extractiong into zip files
    choices5 = ("Extract Files","Compress Files","Back to Main Menu")
    file_task = gui.choicebox("Choose task:", title, choices5)
    if file_task == "Back to Main Menu":
        break
    if file_task == "Compress Files":
        zip_name = gui.enterbox("Enter the name of ZIP file to create (e.g., output.zip):")
        if not zip_name.endswith(".zip"):
            zip_name += ".zip"
        file_paths = gui.fileopenbox("Enter the full paths of files to compress:","Select files",multiple=True)
        if file_paths:
         with zipfile.ZipFile(zip_name, 'w') as zipf:
            for file in file_paths:
                if file and os.path.exists(file):
                    zipf.write(file)
                    print(f"Compressed: {file}")
                else:
                    print(f"File not found or empty: {file}")
         print(f"All files zipped into {zip_name}")
    if file_task == "Extract Files":
        try:
            zip_name = gui.enterbox("Enter the name of the ZIP file to extract: ")
            extract_folder = gui.enterbox("Enter folder to extract files to: ")
            os.makedirs(extract_folder, exist_ok=True)
            with zipfile.ZipFile(zip_name, 'r') as zipf:
                zipf.extractall(extract_folder)
                print(f"Files extracted to {extract_folder}")
        except FileNotFoundError:
            print("Zip file not found.")
 if user_c == "Surprise Me":
    surprises = [
        "💡 Did you know? Python was named after Monty Python!",
        "🎯 Productivity Tip: Organize your files weekly!",
        "📊 Data Tip: Always back up your data before cleaning!",
        "📁 Life’s too short for messy folders.",
        "🔒 Use strong passwords. Like... really strong. 🧠",
        "📂 That file you lost? It's probably in Downloads. Again.",
        "🧹 Clear your mind. And your desktop.",
    ]
    choicesx = ("Random facts", "Rock paper scissor","Capitals Quiz","Coin toss","Back to Main Menu")
    choices6 = gui.choicebox("Choose task:", title, choicesx)
    if choices6 == "Back to Main Menu":
            break
    elif choices6 == "Random facts":
            gui.msgbox(random.choice(surprises), "Here's your surprise!")
    elif choices6 == "Rock paper scissor":
            def play_game():
                choices = ['rock', 'paper', 'scissors']
                computer = random.choice(choices)
                player = gui.enterbox("Enter rock, paper, or scissors: ").lower()        
                while player not in choices:
                    player = gui.enterbox("Invalid input. Enter rock, paper, or scissors: ").lower()
                    continue
                if player == computer:
                    gui.msgbox(f"since both player and computer entered {player},{computer} it is tie")
                    gui.msgbox("Tie!")
                elif (player == "rock" and computer == "scissors") or (player == "paper" and computer == "rock") or (player == "scissors" and computer == "paper"):
                    gui.msgbox(f"since computer put {computer} you win")
                    gui.msgbox("You win!")
                else:
                    gui.msgbox(f"Since computer put {computer} it wins")
                    gui.msgbox("Computer wins!")
            play_game()
            def option():
             while True:
                option = int (gui.enterbox("Press 1 to continue or 2 to exit : "))      
                if(option ==1):
                    play_game()    
                else:
                    break
            option()
    elif choices6 == "Capitals Quiz":
            capitals= {
                "karnataka": "bengaluru",
                "andhra pradesh" : "amravathi",
                "telengana" : "hyderabad",
                "rajasthan": "jaipur",
                "maharastra": "mumbai",
                "bihar":"patna",
                "tamil nadu":"chennai",
                "mizoram":"aizwal",
                "gujarat":"gandhinagar",
                "kerala" : "thiruvananthapuram",
            }
            state,capital=random.choice(list(capitals.items()))
            while True:
                guess = gui.enterbox(f"what is the capital of'{state}'?").lower()
                if guess == capital.lower():
                    gui.msgbox("Correct! Nice job.")          
                elif guess != capital.lower():
                    gui.msgbox("retry")
                    continue
                num=int(gui.enterbox("press 1 to continue or press 2 to exit "))
                if(num==1):
                    state,capital=random.choice(list(capitals.items()))
                    guess = gui.enterbox(f"what is the capital of'{state}'?").lower()
                    if guess == capital.lower():
                        gui.msgbox("Great!!! go ahead.")
                        state,capital=random.choice(list(capitals.items()))
                    else:
                        gui.msgbox("retry")
                elif(num==2):
                    gui.msgbox("goodbye")
                    break
                else:
                    gui.msgbox("ERROR")
    elif choices6 == "Coin toss":
            input_value = gui.enterbox("Enter heads or tails to start the game")
            x=input_value.lower()
            for x in ["heads", "tails"]:
                    coin_toss = random.choice(["heads","tails"])
            if input_value == coin_toss:
                gui.msgbox("You guessed it right!") 
            else:
                gui.msgbox("You guessed it wrong!")
            num=int(gui.enterbox("press 1 to continue or press 2 to exit "))
            if(num==1):
                    input_value = gui.enterbox("Enter heads or tails to start the game")
                    x=input_value.lower()
                    for x in ["heads", "tails"]:
                        coin_toss = shuffle(["heads","tails"])
                    if input_value == coin_toss:
                        gui.msgbox("You guessed it right!") 
                    else:
                        gui.msgbox("You guessed it wrong!")
            elif(num==2):
                    gui.msgbox("goodbye")
                    break
 while user_c == "Compression":
    choices5 = ("Extract Files", "Compress Files", "Back to Main Menu")
    file_task = gui.choicebox("Choose task:", title, choices5)
    if file_task == "Back to Main Menu":
        break
    elif file_task == "Compress Files":
        zip_name = gui.enterbox("Enter ZIP filename (e.g., output.zip):")
        if zip_name and not zip_name.endswith(".zip"):
            zip_name += ".zip"
        file_paths = gui.fileopenbox("Select files to compress:", multiple=True)
        if file_paths:
            try:
                with zipfile.ZipFile(zip_name, 'w') as zipf:
                    for file in file_paths:
                        zipf.write(file, arcname=os.path.basename(file))
                gui.msgbox(f"Files compressed into {zip_name} successfully.")
            except Exception as e:
                gui.exceptionbox(f"Error during compression: {e}")

    elif file_task == "Extract Files":
        zip_file = gui.fileopenbox("Select ZIP file to extract:", filetypes=["*.zip"])
        if zip_file:
            extract_to = gui.diropenbox("Select folder to extract files to:")
            try:
                with zipfile.ZipFile(zip_file, 'r') as zipf:
                    zipf.extractall(extract_to)
                gui.msgbox(f"Files extracted to {extract_to}")
            except Exception as e:
                gui.exceptionbox("Error during extraction", str(e))
 while user_c == "Data Cleaning":
    choices6 = ("Drop Empty Rows", "Fill", "Back to Main Menu")
    file_task = gui.choicebox("Choose task:", title, choices6)
    if file_task == "Back to Main Menu":
        break 
    elif file_task == "Drop Empty Rows":
            path = gui.fileopenbox("Choose CSV file")
            df = pd.read_csv(path)
            new_df = df.dropna()
            gui.textbox("Cleaned Data Preview", "Cleaned CSV Data", new_df.to_string())
            df = new_df  # Store cleaned data for export
    elif file_task == "Export Cleaned Data":
            if 'df' in locals():
                file_name = gui.enterbox("Enter new CSV file name (e.g., cleaned.csv):")
                output_path = gui.filesavebox("Save cleaned CSV as:", default=file_name)
                if output_path:
                    df.to_csv(output_path, index=False)
                    gui.msgbox(f"Cleaned data saved as {output_path}")
            else:
                gui.msgbox("No cleaned data available. Perform cleaning first.")
