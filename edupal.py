import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
from datetime import datetime
import random
import time
import threading



class EduPal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EduPal - Your Educational Assistant")
        self.root.geometry("900x700")  # Adjusted window size
        self.root.minsize(800, 600)  # Set minimum window size
        
        # Add app icon if available
        try:
            self.root.iconbitmap("edupal_icon.ico")
        except:
            pass
            
        # For theme customization
        self.accent_color = "#2A7FFF"  # Default blue accent
        self.is_dark_mode = False
        
        # Theme colors
        self.light_theme = {
            "bg_primary": "#F0F2F5",      # Light background
            "bg_secondary": "#FFFFFF",    # White elements
            "text_primary": "#333333",    # Dark text
            "text_secondary": "#666666",  # Gray text
            "text_inverse": "#FFFFFF",    # White text (for buttons)
            "input_bg": "#FFFFFF",        # Input background
            "input_text": "#333333",      # Input text
            "sidebar_bg": "#E8ECF0",      # Sidebar background
            "hover_bg": "#E8E8E8"         # Hover background
        }
        
        self.dark_theme = {
            "bg_primary": "#1E1E1E",      # Dark background
            "bg_secondary": "#2D2D30",    # Slightly lighter dark
            "text_primary": "#E8E8E8",    # Light text
            "text_secondary": "#BBBBBB",  # Gray text
            "text_inverse": "#FFFFFF",    # White text
            "input_bg": "#3E3E42",        # Input background
            "input_text": "#FFFFFF",      # Input text
            "sidebar_bg": "#252526",      # Sidebar background
            "hover_bg": "#3E3E42"         # Hover background
        }
        
        # Current theme - defaults to light
        self.theme = self.light_theme.copy()
        
        # Apply theme to root
        self.root.configure(bg=self.theme["bg_primary"])
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)  # Sidebar
        self.root.grid_columnconfigure(1, weight=3)  # Main content
        self.root.grid_rowconfigure(0, weight=1)
        
        # Initialize settings
        self.settings_file = "settings.json"
        self.settings = {}
        self.load_settings()
        
        # Load theme from settings
        self.accent_color = self.settings.get("accent_color", self.accent_color)
        self.is_dark_mode = self.settings.get("dark_mode", False)
        
        # Update current theme based on settings
        if self.is_dark_mode:
            self.theme = self.dark_theme.copy()
        else:
            self.theme = self.light_theme.copy()
        
        # Apply theme to root
        self.root.configure(bg=self.theme["bg_primary"])
        
        # Try to load configuration if it exists
        self.cohere_api_key = None
        try:
            config_file = "config.json"
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.cohere_api_key = config.get("cohere_api_key")
        except Exception as e:
            print(f"Warning: Could not load configuration: {e}")
        
        # Show login screen first
        self.show_login()
        
    def load_settings(self):
        # Default settings
        self.settings = {
            "accent_color": self.accent_color,
            "theme_color": self.accent_color,
            "dark_mode": False,
        }
        
        # Try to load from file
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
            
        # Apply loaded settings
        if "accent_color" in self.settings:
            self.accent_color = self.settings["accent_color"]
            
        if "dark_mode" in self.settings:
            self.is_dark_mode = self.settings["dark_mode"]
            if self.is_dark_mode:
                self.theme = self.dark_theme.copy()
            else:
                self.theme = self.light_theme.copy()
        
        # Save settings
        self.save_settings()
        
    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

    def show_login(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create login frame with gradient effect
        login_frame = tk.Frame(self.root, bg=self.theme["bg_primary"], padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title = tk.Label(login_frame, text="Welcome to EduPal ", 
                        font=("Arial", 24, "bold"), bg=self.theme["bg_primary"], fg=self.accent_color)
        title.pack(pady=20)

        # Username
        username_label = tk.Label(login_frame, text="Username:", 
                                font=("Arial", 12), bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
        username_label.pack()
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), 
                                     bg=self.theme["input_bg"], fg=self.theme["input_text"])
        self.username_entry.pack(pady=5)

        # Password
        password_label = tk.Label(login_frame, text="Password:", 
                                font=("Arial", 12), bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
        password_label.pack()
        self.password_entry = tk.Entry(login_frame, show="•", font=("Arial", 12),
                                     bg=self.theme["input_bg"], fg=self.theme["input_text"])
        self.password_entry.pack(pady=5)

        # Login button
        login_button = tk.Button(login_frame, text="Login", 
                               command=self.verify_login,
                               bg=self.accent_color, fg=self.theme["text_inverse"],
                               font=("Arial", 12, "bold"),
                               padx=30, pady=5)
        login_button.pack(pady=20)

        # Bind Enter key to login button
        self.root.bind('<Return>', lambda event: self.verify_login())
        
        # Status text at the bottom
        status_text = tk.Label(login_frame, text="Default Login: username 'student', password 'learn123'",
                            font=("Arial", 9), bg=self.theme["bg_primary"], fg=self.theme["text_secondary"])
        status_text.pack(pady=(20, 0))

        # Auto focus on username
        self.username_entry.focus()

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "student" and password == "learn123":
            self.root.unbind('<Return>')
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials! \nPlease try again.")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()

    def show_dashboard(self):
        # Clear widgets from main area
        for widget in self.root.grid_slaves(row=0, column=1):
            if widget:
                widget.destroy()
        
        # Configure root background
        self.root.configure(bg=self.theme["bg_primary"])
        
        # Add navigation sidebar
        sidebar = tk.Frame(self.root, bg=self.theme["sidebar_bg"], width=200)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # App logo/name
        app_label = tk.Label(sidebar, text="EduPal", 
                           font=("Arial", 18, "bold"), 
                           bg=self.theme["sidebar_bg"], fg=self.accent_color)
        app_label.pack(pady=(20, 30))
        
        # Main content area
        main_content = tk.Frame(self.root, bg=self.theme["bg_primary"], padx=20, pady=20)
        main_content.grid(row=0, column=1, sticky="nsew")

        # Add features buttons
        features = [
            ("AI Essay Writer ", self.show_essay_writer),
            ("AI Assistant ", self.show_study_buddy),
            ("Study Timer ", self.show_study_timer),
            ("ToDo List ", self.show_todo_list),
            ("Theme Settings ", self.show_theme_settings),
            ("Random Advice", self.show_random_advice_window),  # New button
            ("Calculator", self.show_calculator)  # New button
        ]

        for i, (text, command) in enumerate(features):
            btn = tk.Button(sidebar, text=text, command=command,
                          font=("Arial", 12), bg=self.theme["sidebar_bg"], fg=self.accent_color,
                          padx=20, pady=10, width=20)
            btn.pack(pady=10)

        # Quick ideas section
        ideas_frame = tk.LabelFrame(main_content, text="Quick Ideas ", 
                                  font=("Arial", 12, "bold"), bg=self.theme["bg_primary"], 
                                  fg=self.theme["text_primary"])
        ideas_frame.pack(fill="x", pady=20)

        self.ideas_text = tk.Text(ideas_frame, height=4, font=("Arial", 12),
                                wrap=tk.WORD, bg=self.theme["input_bg"])
        self.ideas_text.pack(fill="x", padx=10, pady=10)
        
        # Insert some starter ideas
        ideas = [
            "Create study flashcards for upcoming test",
            "Research topic for next essay",
            "Organize notes from today's lecture",
            "Review chapter summaries"
        ]
        random_idea = random.choice(ideas)
        self.ideas_text.insert("1.0", random_idea)
        
        # Progress bar
        progress_frame = tk.LabelFrame(main_content, text="Daily Progress ",
                                     font=("Arial", 12, "bold"), bg=self.theme["bg_primary"],
                                     fg=self.theme["text_primary"])
        progress_frame.pack(fill="x", pady=20)
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, 
                                         mode='determinate', value=50)
        self.progress_bar.pack(padx=10, pady=10)
        
        # Date and greeting
        current_time = datetime.now()
        greeting = "Good morning" if 5 <= current_time.hour < 12 else "Good afternoon" if 12 <= current_time.hour < 18 else "Good evening"
        date_str = current_time.strftime("%A, %B %d, %Y")
        
        greeting_label = tk.Label(main_content, text=f"{greeting}! Today is {date_str}",
                                font=("Arial", 14), bg=self.theme["bg_primary"], fg=self.accent_color)
        greeting_label.pack(pady=10)

        # Help button
        help_btn = tk.Button(main_content, text="Help ",
                           command=self.show_help,
                           font=("Arial", 10),
                           bg=self.accent_color, fg=self.theme["text_inverse"])
        help_btn.pack(side="bottom", anchor="se", pady=10)

    def show_random_advice_window(self):
        """Open a new window to display random advice."""
        advice_window = tk.Toplevel(self.root)
        advice_window.title("Random Advice")
        advice_window.geometry("400x300")
        advice_window.configure(bg=self.theme["bg_primary"])

        advice_label = tk.Label(advice_window, text="Random Advice", 
                                font=("Arial", 16, "bold"), bg=self.theme["bg_primary"], fg=self.accent_color)
        advice_label.pack(pady=10)

        advice_text = tk.Text(advice_window, wrap=tk.WORD, font=("Arial", 12),
                              bg=self.theme["input_bg"], fg=self.theme["input_text"], height=10)
        advice_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Generate random advice
        tips = [
            "Break large study tasks into smaller, manageable chunks.",
            "Use active recall instead of passive re-reading.",
            "Teach what you've learned to someone else to reinforce your knowledge.",
            "Take short breaks every 25-30 minutes of focused study.",
            "Create mind maps to visualize connections between concepts.",
            "Study in different locations to improve retention.",
            "Review material before sleep to enhance memory consolidation.",
            "Use spaced repetition to review content at optimal intervals.",
            "Stay hydrated and maintain healthy snacks during study sessions.",
            "Set specific goals for each study session"
        ]
        random_tip = random.choice(tips)
        advice_text.insert("1.0", random_tip)
        advice_text.config(state="disabled")

        close_button = tk.Button(advice_window, text="Close", command=advice_window.destroy,
                                 bg=self.accent_color, fg=self.theme["text_inverse"], font=("Arial", 12))
        close_button.pack(pady=10)

    def show_essay_writer(self):
        # Clear main content area
        for widget in self.root.winfo_children():
            if widget.grid_info().get('column') == 1:
                widget.destroy()

        # Create a frame for the essay writer
        essay_frame = tk.Frame(self.root, bg=self.theme["bg_primary"], padx=20, pady=20)
        essay_frame.grid(row=0, column=1, sticky="nsew")
        
        # Configure the grid to expand with window resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Make essay_frame expandable
        essay_frame.grid_rowconfigure(0, weight=1)
        essay_frame.grid_columnconfigure(0, weight=1)

        # Title
        title = tk.Label(essay_frame, text="AI Essay Writer ", 
                         font=("Arial", 16, "bold"), bg=self.theme["bg_primary"], fg=self.accent_color)
        title.pack(pady=10)

        # Topic input
        topic_label = tk.Label(essay_frame, text="Essay Topic:", 
                              font=("Arial", 12), bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
        topic_label.pack(anchor="w", pady=(10, 0))
        self.topic_entry = tk.Entry(essay_frame, font=("Arial", 12), 
                                     bg=self.theme["input_bg"], fg=self.theme["input_text"])
        self.topic_entry.pack(pady=(0, 10), fill="x")

        # Word count slider
        word_count_frame = tk.Frame(essay_frame, bg=self.theme["bg_primary"])
        word_count_frame.pack(fill="x", pady=10)
        
        word_count_label = tk.Label(word_count_frame, text="Word Count: ", 
                                  font=("Arial", 12), bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
        word_count_label.pack(side="left")
        
        self.word_count_var = tk.IntVar(value=self.settings.get("last_word_count", 250))
        
        def update_word_count_label(val):
            word_count_value_label.config(text=f"{int(val)} words")
            self.settings["last_word_count"] = int(val)
            self.save_settings()
            
        word_count_slider = tk.Scale(word_count_frame, from_=100, to=500, 
                                    orient="horizontal", length=300, 
                                    variable=self.word_count_var,
                                    command=update_word_count_label,
                                    bg=self.theme["bg_primary"], highlightthickness=0)
        word_count_slider.pack(side="left", padx=10)
        
        word_count_value_label = tk.Label(word_count_frame, 
                                        text=f"{self.word_count_var.get()} words", 
                                        font=("Arial", 12), bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
        word_count_value_label.pack(side="left")

        # Add headers/bullet points options
        format_frame = tk.Frame(essay_frame, bg=self.theme["bg_primary"])
        format_frame.pack(fill="x", pady=10)
        
        format_label = tk.Label(format_frame, text="Format Options:", 
                               font=("Arial", 12), bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
        format_label.pack(anchor="w")
        
        self.headers_var = tk.BooleanVar(value=True)
        headers_check = tk.Checkbutton(format_frame, text="Add Headers", 
                                         variable=self.headers_var, 
                                         font=("Arial", 11), bg=self.theme["bg_primary"], fg=self.theme["text_primary"],
                                         selectcolor=self.theme["bg_secondary"], state=tk.NORMAL)
        headers_check.pack(anchor="w")
        
        self.bullets_var = tk.BooleanVar(value=True)
        bullets_check = tk.Checkbutton(format_frame, text="Add Bullet Points", 
                                         variable=self.bullets_var, 
                                         font=("Arial", 11), bg=self.theme["bg_primary"], fg=self.theme["text_primary"],
                                         selectcolor=self.theme["bg_secondary"], state=tk.NORMAL)
        bullets_check.pack(anchor="w")

        # Generate button
        generate_button = tk.Button(essay_frame, text="Generate Essay", 
                                  command=self.generate_essay,
                                  bg=self.accent_color, fg=self.theme["text_inverse"],
                                  font=("Arial", 12, "bold"),
                                  padx=20, pady=5)
        generate_button.pack(pady=20)

        # Result text area
        result_label = tk.Label(essay_frame, text="Generated Essay:", 
                              font=("Arial", 12, "bold"), bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
        result_label.pack(anchor="w", pady=(10, 0))
        
        # Create a container frame that will expand with the window
        result_container = tk.Frame(essay_frame, bg=self.theme["bg_primary"])
        result_container.pack(fill="both", expand=True, pady=10)
        
        # Set minimum height for the result frame
        result_frame = tk.Frame(result_container, bg=self.theme["input_bg"], bd=1, relief="solid", height=300)
        result_frame.pack(fill="both", expand=True)
        result_frame.pack_propagate(False)  # Prevent the frame from shrinking below its set height
        
        # Text widget with scrollbar
        self.essay_result = tk.Text(result_frame, font=("Arial", 12), 
                                  wrap=tk.WORD, padx=10, pady=10,
                                  bg=self.theme["input_bg"], fg=self.theme["input_text"])
        self.essay_result.pack(side="left", fill="both", expand=True)
        
        essay_scrollbar = tk.Scrollbar(result_frame, command=self.essay_result.yview)
        essay_scrollbar.pack(side="right", fill="y")
        self.essay_result.config(yscrollcommand=essay_scrollbar.set)

        # Export button
        export_button = tk.Button(essay_frame, text="Export as TXT ", 
                                command=self.export_essay,
                                bg=self.accent_color, fg=self.theme["text_inverse"],
                                font=("Arial", 12),
                                padx=20, pady=5)
        export_button.pack(pady=10)

    def generate_essay(self):
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showerror("Error", "Please enter a topic! ")
            return
            
        word_count = self.word_count_var.get()
        add_headers = self.headers_var.get()
        add_bullets = self.bullets_var.get()
        
        # Update status
        self.essay_result.delete("1.0", tk.END)
        self.essay_result.insert("1.0", "Generating your essay... Please wait...")
        self.root.update()
        
        # Save the word count preference
        self.settings["last_word_count"] = word_count
        self.save_settings()
        
        # Generate essay in a separate thread to avoid freezing UI
        def generate_essay_thread():
            try:
                if not self.cohere_api_key:
                    # Simulate essay generation if no API key
                    time.sleep(2)  # Simulate API call delay
                    essay_text = self.generate_sample_essay(topic, word_count, add_headers, add_bullets)
                else:
                    # Import cohere here to avoid import errors if not available
                    import cohere
                    
                    # Configure the prompt based on format options
                    prompt = f"Write an essay about {topic} that is approximately {word_count} words long."
                    if add_headers:
                        prompt += " Structure it with a clear title at the top, and include section headers like 'Introduction', 'Main Points', and 'Conclusion'."
                    if add_bullets:
                        prompt += " Use bullet points (with • symbols) to list key information and arguments."
                        
                    # Call the Cohere API
                    client = cohere.Client(self.cohere_api_key)
                    response = client.generate(
                        prompt=prompt,
                        max_tokens=word_count * 2,
                        temperature=0.7,
                        return_likelihoods="NONE"
                    )
                    essay_text = response.generations[0].text
                
                # Post-process the essay text to enhance formatting
                if add_headers and "TITLE:" not in essay_text and "Title:" not in essay_text:
                    title = topic.upper()
                    essay_text = f"TITLE: {title}\n\n{essay_text}"
                    
                if add_bullets and "-" not in essay_text and "•" not in essay_text:
                    # Add some bullet points if the API didn't include any
                    lines = essay_text.split('\n')
                    for i in range(len(lines)):
                        if "key point" in lines[i].lower() or "important" in lines[i].lower():
                            lines[i] = "• " + lines[i]
                    essay_text = '\n'.join(lines)
                    
                # Update UI in main thread
                self.root.after(0, lambda: self.update_essay_result(essay_text))
                
            except Exception as e:
                error_message = str(e)
                self.root.after(0, lambda: self.handle_api_error(error_message))
        
        threading.Thread(target=generate_essay_thread, daemon=True).start()
        
    def generate_sample_essay(self, topic, word_count, add_headers, add_bullets):
        """Generate a sample essay when the API key is not available"""
        
        # Base text structure
        intro = f"Introduction to {topic}\n\nAn essay exploring the various aspects of {topic}. This topic is interesting for several reasons and merits thorough examination."
        
        body_sections = [
            f"Understanding {topic} requires analysis of its key components. Researchers have identified several factors that contribute to this subject.",
            f"The history of {topic} provides valuable context. Over time, significant developments have shaped our understanding of this area.",
            f"When considering the practical applications of {topic}, we can identify numerous examples across different domains.",
            f"Recent advances related to {topic} have opened new possibilities for research and development in this field."
        ]
        
        conclusion = f"In conclusion, {topic} represents an important area of study with numerous implications. Further research and practical applications will continue to enhance our understanding."
        
        # Build the essay
        essay_parts = []
        
        # Add introduction
        if add_headers:
            essay_parts.append("# Introduction")
        essay_parts.append(intro)
        
        # Add body sections
        for i, section in enumerate(body_sections[:3]):  # Limit to 3 sections for shorter essays
            if add_headers:
                essay_parts.append(f"\n# Section {i+1}")
            essay_parts.append(section)
            
            # Add bullet points if requested
            if add_bullets:
                essay_parts.append("\nKey points:")
                for j in range(3):
                    point = f"• Important aspect {j+1} related to this section of {topic}"
                    essay_parts.append(point)
        
        # Add conclusion
        if add_headers:
            essay_parts.append("\n# Conclusion")
        essay_parts.append(conclusion)
        
        # Join all parts
        return "\n\n".join(essay_parts)

    def handle_api_error(self, error_message):
        self.essay_result.delete("1.0", tk.END)
        self.essay_result.insert("1.0", f"Error: {error_message}\n\n")
        self.essay_result.insert(tk.END, "Offline mode: Here's a sample essay structure instead:\n\n")
        self.essay_result.insert(tk.END, f"# Introduction to {self.topic_entry.get()}\n\n")
        self.essay_result.insert(tk.END, "• Key point 1\n• Key point 2\n• Key point 3\n\n")
        self.essay_result.insert(tk.END, "# Main Arguments\n\n")
        self.essay_result.insert(tk.END, "Write your main arguments here...\n\n")
        self.essay_result.insert(tk.END, "# Conclusion\n\n")
        self.essay_result.insert(tk.END, "Write your conclusion here...\n")

    def update_essay_result(self, essay_text):
        self.essay_result.delete("1.0", tk.END)
        
        # Configure text tags for formatting
        self.essay_result.tag_configure("header", font=("Arial", 14, "bold"))
        self.essay_result.tag_configure("bullet", lmargin1=20, lmargin2=40)
        
        # Process text for better formatting
        lines = essay_text.split('\n')
        for line in lines:
            # Check if this line is a header (starts with # or is all caps)
            if line.strip().startswith('#') or (line.strip().isupper() and len(line.strip()) > 3):
                self.essay_result.insert(tk.END, line + "\n", "header")
            
            # Check if this line is a bullet point
            elif line.strip().startswith('•') or line.strip().startswith('-') or line.strip().startswith('*'):
                # Format as bullet point
                self.essay_result.insert(tk.END, line + "\n", "bullet")
            
            # Regular text
            else:
                self.essay_result.insert(tk.END, line + "\n")
        
        # Play success sound
        messagebox.showinfo("Success", "Essay generated successfully! ")

    def export_essay(self):
        essay_text = self.essay_result.get("1.0", tk.END)
        if not essay_text.strip() or essay_text.strip() == "Generating your essay... Please wait...":
            messagebox.showerror("Error", "No essay to export! ")
            return
            
        # Create timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic = self.topic_entry.get().replace(" ", "_")[:20]  # Limit length and remove spaces
        filename = f"essay_{topic}_{timestamp}.txt"
        
        try:
            with open(filename, "w") as f:
                f.write(essay_text)
            messagebox.showinfo("Success", f"Essay exported as '{filename}' ")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export essay: {str(e)} ")

    def show_study_buddy(self):
        # Clear main content area
        for widget in self.root.winfo_children():
            if widget.grid_info().get('column') == 1:
                widget.destroy()

        # Create a frame for the chatbot
        chat_frame = tk.Frame(self.root, bg=self.theme["bg_primary"], padx=20, pady=20)
        chat_frame.grid(row=0, column=1, sticky="nsew")

        # Title
        title = tk.Label(chat_frame, text="AI Assistant ", 
                       font=("Arial", 16, "bold"), bg=self.theme["bg_primary"], fg=self.accent_color)
        title.pack(pady=10)
        
        # Chat history section
        history_label = tk.Label(chat_frame, text="Chat History:", 
                             font=("Arial", 12, "bold"), bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
        history_label.pack(anchor="w", pady=(10, 0))
        
        history_frame = tk.Frame(chat_frame, bg=self.theme["bg_primary"])
        history_frame.pack(fill="both", expand=True, pady=10)
        
        self.chat_history = tk.Text(history_frame, height=15, width=60, 
                                  font=("Arial", 12), wrap=tk.WORD,
                                  bg=self.theme["input_bg"], fg=self.theme["text_primary"],
                                  state="disabled")
        self.chat_history.pack(side="left", fill="both", expand=True)
        
        history_scrollbar = tk.Scrollbar(history_frame, command=self.chat_history.yview)
        history_scrollbar.pack(side="right", fill="y")
        self.chat_history.config(yscrollcommand=history_scrollbar.set)
        
        # Add a welcome message
        self.update_chat_history("AI Assistant", "Hello! I'm your AI assistant. How can I help you with your studies today?")
        
        # Input section
        input_frame = tk.Frame(chat_frame, bg=self.theme["bg_primary"])
        input_frame.pack(fill="x", pady=10)
        
        input_label = tk.Label(input_frame, text="Your question:", 
                            font=("Arial", 12), bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
        input_label.pack(side="left", padx=(0, 10))
        
        self.chat_input = tk.Entry(input_frame, font=("Arial", 12), width=50,
                                 bg=self.theme["input_bg"], fg=self.theme["input_text"])
        self.chat_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.chat_input.bind("<Return>", lambda e: self.send_message())
        
        send_button = tk.Button(input_frame, text="Send", 
                              command=self.send_message,
                              bg=self.accent_color, fg=self.theme["text_inverse"],
                              font=("Arial", 12),
                              padx=10, pady=5)
        send_button.pack(side="right")
        
        if SPEECH_RECOGNITION_AVAILABLE:
            voice_button = tk.Button(input_frame, text="", 
                                   command=self.voice_input,
                                   bg=self.accent_color, fg=self.theme["text_inverse"],
                                   font=("Arial", 12),
                                   padx=5, pady=5)
            voice_button.pack(side="right", padx=5)
        
        # Auto focus on input
        self.chat_input.focus()

    def send_message(self):
        user_message = self.chat_input.get().strip()
        if not user_message:
            return
            
        # Clear input field
        self.chat_input.delete(0, tk.END)
        
        # Add user message to chat
        self.update_chat_history("You", user_message)
        
        # Check for basic math operations
        if self.is_math_question(user_message):
            try:
                result = self.evaluate_math(user_message)
                self.root.after(500, lambda: self.update_chat_history("AI Assistant", f"The answer is {result}"))
                return
            except:
                pass  # Fall back to normal response if math evaluation fails
        
        # Simulate AI response with threading to avoid UI freeze
        threading.Thread(target=self.get_ai_response, args=(user_message,), daemon=True).start()
    
    def is_math_question(self, message):
        """Check if the message is a basic math question"""
        # Remove spaces and convert to lowercase
        message = message.lower().replace(" ", "")
        
        # Check for common math operators (+, -, *, /, ^)
        has_operator = any(op in message for op in ['+', '-', '*', '/', '^'])
        
        # Check if it's mostly numbers and operators
        is_mostly_math = sum(c.isdigit() or c in '+-*/^().' for c in message) > len(message) * 0.5
        
        return has_operator and is_mostly_math
    
    def evaluate_math(self, expression):
        """Safely evaluate a math expression"""
        # Replace ^ with ** for exponentiation
        expression = expression.replace('^', '**')
        
        # Remove all characters except numbers, operators, and parentheses
        expression = ''.join(c for c in expression if c.isdigit() or c in '+-*/().** ')
        
        # Evaluate using a safe approach
        try:
            # Use ast.literal_eval for safety
            result = eval(expression)
            return result
        except:
            raise ValueError("Could not evaluate math expression")
    
    def update_chat_history(self, sender, message):
        self.chat_history.config(state="normal", wrap=tk.WORD)  # Add word wrap
        if sender:
            timestamp = datetime.now().strftime("%H:%M")
            self.chat_history.insert(tk.END, f"\n{timestamp} {sender}: \n", "sender")
            self.chat_history.insert(tk.END, f"{message}\n\n", "message")
        else:
            self.chat_history.insert(tk.END, f"{message}\n", "system")
        self.chat_history.see(tk.END)  # Auto-scroll to bottom
        self.chat_history.config(state="disabled")
        
        # Configure tags for better visibility in dark mode
        if self.is_dark_mode:
            self.chat_history.tag_config("sender", foreground="#7ADBFC", font=("Arial", 12, "bold"))
            self.chat_history.tag_config("message", foreground="#E8E8E8") 
        else:
            self.chat_history.tag_config("sender", foreground="#0066CC", font=("Arial", 12, "bold"))
            self.chat_history.tag_config("message", foreground="#333333")

    def get_ai_response(self, user_message):
        """Get response from AI model."""
        try:
            if not self.cohere_api_key:
                raise ValueError("Cohere API key is missing. Please configure it in 'config.json'.")

            import cohere
            co = cohere.Client(self.cohere_api_key)
            
            # Using generate instead of chat (simpler API)
            prompt = f"You are a helpful educational AI assistant. User: {user_message}\nAI Assistant:"
            response = co.generate(
                prompt=prompt,
                max_tokens=300,
                temperature=0.7,
                return_likelihoods="NONE"
            )
            
            # Get the generated text from the first generation
            bot_response = response.generations[0].text.strip()
            self.root.after(0, lambda: self.update_chat_history("AI Assistant", bot_response))
        except Exception as e:
            error_message = f"API Error: {str(e)}\nPlease check your internet connection and API key"
            self.root.after(0, lambda: self.update_chat_history("System", error_message))

    def voice_input(self):
        if not SPEECH_RECOGNITION_AVAILABLE:
            messagebox.showerror("Error", "Speech recognition is not available!")
            return
            
        try:
            messagebox.showinfo("Voice Input", "Please speak into your microphone...")
            
            # Initialize recognizer
            r = sr.Recognizer()
            
            # Use microphone as source
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=5)
                
            # Recognize speech
            text = r.recognize_google(audio)
            
            # Update input field
            self.chat_input.delete(0, tk.END)
            self.chat_input.insert(0, text)
            
        except sr.RequestError:
            messagebox.showerror("Error", "Speech service is unavailable!")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio!")
        except Exception as e:
            messagebox.showerror("Error", f"Voice input error: {str(e)}")
    
    def show_random_tip(self):
        tips = [
            "Break large study tasks into smaller, manageable chunks",
            "Use active recall instead of passive re-reading",
            "Teach what you've learned to someone else to reinforce your knowledge",
            "Take short breaks every 25-30 minutes of focused study",
            "Create mind maps to visualize connections between concepts",
            "Study in different locations to improve retention",
            "Review material before sleep to enhance memory consolidation",
            "Use spaced repetition to review content at optimal intervals",
            "Stay hydrated and maintain healthy snacks during study sessions",
            "Set specific goals for each study session"
        ]
        
        tip = random.choice(tips)
        messagebox.showinfo("Lightbulb Moment ", tip)

    def show_help(self):
        help_text = """
        EduPal Help Guide:
        
        • Login: Use username 'student' and password 'learn123'
        • AI Essay Writer: Get AI-powered essay suggestions
        • AI Assistant: Chat with AI for homework help
        • Lightbulb Moment: Get random study tips
        
        Need more help? Contact support@edupal.com
        """
        messagebox.showinfo("Help Guide", help_text)

    def show_study_timer(self):
        # Clear main content area
        for widget in self.root.grid_slaves(row=0, column=1):
            if widget:
                widget.destroy()

        # Create a frame for the timer
        timer_frame = tk.Frame(self.root, bg=self.theme["bg_primary"], padx=20, pady=20)
        timer_frame.grid(row=0, column=1, sticky="nsew")
        timer_frame._name = "timer_frame"  # For identifying current screen

        # Title
        title = tk.Label(timer_frame, text="Study Timer ", 
                       font=("Arial", 16, "bold"), bg=self.theme["bg_primary"], fg=self.accent_color)
        title.pack(pady=10)
        
        # Timer display
        display_frame = tk.Frame(timer_frame, bg=self.theme["bg_primary"])
        display_frame.pack(pady=20)
        
        self.time_display = tk.Label(display_frame, text="25:00", 
                                   font=("Arial", 48, "bold"), bg=self.theme["bg_primary"], 
                                   fg=self.theme["text_primary"])
        self.time_display.pack()
        
        self.status_label = tk.Label(display_frame, text="Ready to start", 
                                   font=("Arial", 14), bg=self.theme["bg_primary"], 
                                   fg=self.theme["text_primary"])
        self.status_label.pack(pady=10)
        
        # Timer controls
        controls_frame = tk.Frame(timer_frame, bg=self.theme["bg_primary"])
        controls_frame.pack(pady=20)
        
        self.start_button = tk.Button(controls_frame, text="Start", 
                                    command=self.start_timer,
                                    bg="#4CAF50", fg=self.theme["text_inverse"],
                                    font=("Arial", 14),
                                    padx=20, pady=10)
        self.start_button.pack(side="left", padx=5)
        
        self.pause_button = tk.Button(controls_frame, text="Pause", 
                                    command=self.pause_timer,
                                    bg=self.accent_color, fg=self.theme["text_inverse"],
                                    font=("Arial", 14),
                                    padx=20, pady=10,
                                    state="disabled")
        self.pause_button.pack(side="left", padx=5)
        
        self.reset_button = tk.Button(controls_frame, text="Reset", 
                                    command=self.reset_timer,
                                    bg="#FF5722", fg=self.theme["text_inverse"],
                                    font=("Arial", 14),
                                    padx=20, pady=10)
        self.reset_button.pack(side="left", padx=5)
        
        # Timer settings
        settings_frame = tk.LabelFrame(timer_frame, text="Timer Settings", 
                                      font=("Arial", 12, "bold"), bg=self.theme["bg_primary"],
                                      fg=self.theme["text_primary"])
        settings_frame.pack(fill="x", pady=20)
        
        # Work duration setting
        work_frame = tk.Frame(settings_frame, bg=self.theme["bg_primary"])
        work_frame.pack(fill="x", pady=10)
        
        work_label = tk.Label(work_frame, text="Work Duration (min): ", 
                             font=("Arial", 12), bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
        work_label.pack(side="left", padx=10)
        
        self.work_min_var = tk.IntVar(value=25)
        work_spin = tk.Spinbox(work_frame, from_=1, to=60, width=5, 
                             textvariable=self.work_min_var,
                             bg=self.theme["input_bg"], fg=self.theme["input_text"])
        work_spin.pack(side="left")
        
        # Break duration setting
        break_frame = tk.Frame(settings_frame, bg=self.theme["bg_primary"])
        break_frame.pack(fill="x", pady=10)
        
        break_label = tk.Label(break_frame, text="Break Duration (min): ", 
                              font=("Arial", 12), bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
        break_label.pack(side="left", padx=10)
        
        self.break_min_var = tk.IntVar(value=5)
        break_spin = tk.Spinbox(break_frame, from_=1, to=30, width=5, 
                              textvariable=self.break_min_var,
                              bg=self.theme["input_bg"], fg=self.theme["input_text"])
        break_spin.pack(side="left")
        
        # Session log
        log_frame = tk.LabelFrame(timer_frame, text="Work Session Log", 
                                font=("Arial", 12, "bold"), bg=self.theme["bg_primary"],
                                fg=self.theme["text_primary"])
        log_frame.pack(fill="both", expand=True, pady=20)
        
        self.session_log = tk.Text(log_frame, height=8, font=("Arial", 12), 
                                 wrap=tk.WORD, bg=self.theme["input_bg"], fg=self.theme["text_primary"])
        self.session_log.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        log_scrollbar = tk.Scrollbar(log_frame, command=self.session_log.yview)
        log_scrollbar.pack(side="right", fill="y")
        self.session_log.config(yscrollcommand=log_scrollbar.set)
        
        # Add initial entry to session log
        timestamp = datetime.now().strftime("%H:%M")
        self.session_log.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.session_log.insert(tk.END, "Study Timer Ready\n", "heading")
        self.session_log.config(state="disabled")

    def log_session_event(self, event):
        """Add an event to the session log with timestamp"""
        self.session_log.config(state="normal")
        timestamp = datetime.now().strftime("%H:%M")
        self.session_log.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.session_log.insert(tk.END, f"{event}\n", "message")
        self.session_log.see(tk.END)
        self.session_log.config(state="disabled")
        
        # Configure tags for better visibility in dark mode
        self.session_log.tag_config("timestamp", foreground="#7ADBFC", font=("Arial", 12, "bold"))
        self.session_log.tag_config("heading", foreground="#7ADBFC", font=("Arial", 12, "bold"))
        self.session_log.tag_config("message", foreground="#E8E8E8")

    def start_timer(self):
        if not hasattr(self, "timer_running"):
            self.timer_running = False
        if not self.timer_running:
            self.timer_running = True
            self.start_button.config(state="disabled")
            self.pause_button.config(state="normal")
            self.update_timer()

    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.start_button.config(state="normal", text="Resume")
            self.pause_button.config(state="disabled")
            if hasattr(self, "timer_after_id") and self.timer_after_id:
                self.root.after_cancel(self.timer_after_id)

    def reset_timer(self):
        if hasattr(self, "timer_after_id") and self.timer_after_id:
            self.root.after_cancel(self.timer_after_id)
        self.timer_running = False
        self.current_session_type = "work"
        self.remaining_seconds = self.work_min_var.get() * 60
        self.start_button.config(state="normal", text="Start")
        self.pause_button.config(state="disabled")
        self.update_time_display()

    def update_timer(self):
        if self.timer_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_time_display()
            self.timer_after_id = self.root.after(1000, self.update_timer)
        elif self.timer_running:  # Only trigger completion if actually running
            self.timer_running = False
            self.root.bell()
            if self.current_session_type == "work":
                self.current_session_type = "break"
                self.remaining_seconds = self.break_min_var.get() * 60
                self.status_label.config(text="Break Time! Rest your mind.")
                messagebox.showinfo("Session Complete", "Work session complete! Time for a break.")
            else:
                self.current_session_type = "work"
                self.remaining_seconds = self.work_min_var.get() * 60
                self.status_label.config(text="Work Session")
                messagebox.showinfo("Break Complete", "Break time over! Ready to focus again?")
            self.update_time_display()
            self.start_button.config(state="normal", text="Start")
            self.pause_button.config(state="disabled")

    def update_time_display(self):
        minutes, seconds = divmod(self.remaining_seconds, 60)
        self.time_display.config(text=f"{minutes:02d}:{seconds:02d}")
    
    def show_todo_list(self):
        # Clear main content area
        for widget in self.root.grid_slaves(row=0, column=1):
            if widget:
                widget.destroy()

        # Main frame
        main_frame = tk.Frame(self.root, bg=self.theme["bg_primary"], padx=30, pady=30)
        main_frame.grid(row=0, column=1, sticky="nsew")

        # Title
        title = tk.Label(main_frame, text="To-Do List", 
                        font=("Arial", 16, "bold"), bg=self.theme["bg_primary"], fg=self.accent_color)
        title.pack(pady=10)

        # Task input area
        input_frame = tk.Frame(main_frame, bg=self.theme["bg_primary"])
        input_frame.pack(fill="x", pady=20)

        task_label = tk.Label(input_frame, text="New Task:", 
                            font=("Arial", 12), bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
        task_label.pack(side="left", padx=5)

        self.task_entry = tk.Entry(input_frame, font=("Arial", 12), width=30,
                                 bg=self.theme["input_bg"], fg=self.theme["input_text"])
        self.task_entry.pack(side="left", padx=10, fill="x", expand=True)
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        add_button = tk.Button(input_frame, text="Add Task", 
                             command=self.add_task,
                             bg=self.accent_color, fg=self.theme["text_inverse"],
                             font=("Arial", 12),
                             padx=10, pady=5)
        add_button.pack(side="left", padx=5)

        # Task list area with scrollbar
        task_frame = tk.Frame(main_frame, bg=self.theme["bg_secondary"], bd=1, relief="solid")
        task_frame.pack(fill="both", expand=True, pady=10)

        # Canvas and scrollbar setup for scrolling
        task_canvas = tk.Canvas(task_frame, bg=self.theme["bg_secondary"], highlightthickness=0)
        task_scrollbar = tk.Scrollbar(task_frame, orient="vertical", command=task_canvas.yview)
        task_scrollbar.pack(side="right", fill="y")
        task_canvas.pack(side="left", fill="both", expand=True)
        task_canvas.configure(yscrollcommand=task_scrollbar.set)

        # Frame to hold the tasks inside the canvas
        self.tasks_container = tk.Frame(task_canvas, bg=self.theme["bg_secondary"])
        task_canvas.create_window((0, 0), window=self.tasks_container, anchor="nw", tags="self.tasks_container")
        self.tasks_container.bind("<Configure>", lambda e: task_canvas.configure(scrollregion=task_canvas.bbox("all")))

        # Button to clear completed tasks
        clear_button = tk.Button(main_frame, text="Clear Completed Tasks", 
                               command=self.clear_completed_tasks,
                               bg=self.theme["bg_secondary"], fg=self.accent_color,
                               font=("Arial", 12),
                               padx=10, pady=5)
        clear_button.pack(pady=20)

        # Load saved tasks
        self.load_tasks()

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            # Create task frame 
            task_frame = tk.Frame(self.tasks_container, bg=self.theme["bg_secondary"], bd=1, relief="solid", padx=5, pady=5)
            task_frame.pack(fill="x", pady=2)
            
            # Variable to store check state
            check_var = tk.BooleanVar()
            
            # Task checkbox - FIXED to not call clear_task directly, which was causing the single-task selection issue
            checkbox = tk.Checkbutton(task_frame, variable=check_var, 
                                     bg=self.theme["bg_secondary"], 
                                     selectcolor=self.theme["input_bg"],
                                     command=lambda: self.update_task_state(task_frame, check_var.get(), task_label))
            checkbox.pack(side="left")
            
            # Task text
            task_label = tk.Label(task_frame, text=task_text, wraplength=400, justify="left",
                                font=("Arial", 12), bg=self.theme["bg_secondary"], fg=self.theme["text_primary"])
            task_label.pack(side="left", padx=5, fill="x", expand=True)
            
            # Delete button
            delete_btn = tk.Button(task_frame, text="×", font=("Arial", 12, "bold"),
                                         command=lambda tf=task_frame: self.delete_task(tf),
                                         bg=self.theme["bg_secondary"], fg="red", 
                                         borderwidth=0, padx=5)
            delete_btn.pack(side="right")
            
            # Add to tasks list with various properties
            task_frame.task_text = task_text
            task_frame.check_var = check_var
            task_frame.task_label = task_label
            
            # Clear entry field
            self.task_entry.delete(0, tk.END)
            
            # Save task list
            self.save_tasks()
    
    def update_task_state(self, task_frame, is_checked, task_label):
        """Update the task state when checkbox is clicked"""
        if is_checked:
            # Strike through text when checked
            task_label.configure(font=("Arial", 12, "overstrike"), fg=self.theme["text_secondary"])
        else:
            # Normal text when unchecked
            task_label.configure(font=("Arial", 12), fg=self.theme["text_primary"])
        
        # Save tasks after state change
        self.save_tasks()

    def delete_task(self, task_frame):
        task_frame.destroy()
        self.save_tasks()

    def clear_completed_tasks(self):
        # Remove all checked tasks
        for task_frame in self.tasks_container.winfo_children():
            if hasattr(task_frame, 'check_var') and task_frame.check_var.get():
                task_frame.destroy()
        
        # Save tasks
        self.save_tasks()

    def save_tasks(self):
        tasks = []
        for task_frame in self.tasks_container.winfo_children():
            if hasattr(task_frame, 'task_text'):
                tasks.append({
                    "text": task_frame.task_text,
                    "completed": task_frame.check_var.get()
                })
                
        # Save to file
        try:
            with open("todo_list.json", "w") as f:
                json.dump(tasks, f)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self):
        try:
            if os.path.exists("todo_list.json"):
                with open("todo_list.json", "r") as f:
                    tasks = json.load(f)
                    
                for task in tasks:
                    # Create task frame 
                    task_frame = tk.Frame(self.tasks_container, bg=self.theme["bg_secondary"], bd=1, relief="solid", padx=5, pady=5)
                    task_frame.pack(fill="x", pady=2)
                    
                    # Variable to store check state
                    check_var = tk.BooleanVar(value=task["completed"])
                    
                    # Task checkbox - using update_task_state to allow multiple selections
                    checkbox = tk.Checkbutton(task_frame, variable=check_var, 
                                           bg=self.theme["bg_secondary"], 
                                           selectcolor=self.theme["input_bg"])
                    checkbox.pack(side="left")
                    
                    # Task text
                    task_label = tk.Label(task_frame, text=task["text"], wraplength=400, justify="left",
                                        font=("Arial", 12), bg=self.theme["bg_secondary"], fg=self.theme["text_primary"])
                    task_label.pack(side="left", padx=5, fill="x", expand=True)
                    
                    # Delete button
                    delete_btn = tk.Button(task_frame, text="×", font=("Arial", 12, "bold"),
                                         command=lambda tf=task_frame: self.delete_task(tf),
                                         bg=self.theme["bg_secondary"], fg="red", 
                                         borderwidth=0, padx=5)
                    delete_btn.pack(side="right")
                    
                    # Add to tasks list with various properties
                    task_frame.task_text = task["text"]
                    task_frame.check_var = check_var
                    task_frame.task_label = task_label
                    
                    # Set initial state (strikethrough if completed)
                    if task["completed"]:
                        task_label.configure(font=("Arial", 12, "overstrike"), fg=self.theme["text_secondary"])
                    
                    # Configure the command after all attributes are set
                    checkbox.configure(command=lambda tf=task_frame, cv=check_var, tl=task_label: 
                                      self.update_task_state(tf, cv.get(), tl))
                    
        except Exception as e:
            print(f"Error loading tasks: {e}")
    
    def show_theme_settings(self):
        # Clear main content area
        for widget in self.root.grid_slaves(row=0, column=1):
            if widget:
                widget.destroy()

        # Create a frame for theme settings
        theme_frame = tk.Frame(self.root, bg=self.theme["bg_primary"], padx=20, pady=20)
        theme_frame.grid(row=0, column=1, sticky="nsew")

        # Title
        title = tk.Label(theme_frame, text="Theme Settings ", 
                        font=("Arial", 16, "bold"), bg=self.theme["bg_primary"], fg=self.accent_color)
        title.pack(pady=10)
        
        # Modern container with rounded corners effect
        theme_container = tk.Frame(theme_frame, bg=self.theme["bg_secondary"], padx=25, pady=25, bd=0, relief="flat")
        theme_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add a separator for visual appeal
        separator = ttk.Separator(theme_container, orient="horizontal")
        separator.pack(fill="x", pady=20)
        
        # Dark mode toggle with improved styling
        dark_mode_frame = tk.Frame(theme_container, bg=self.theme["bg_secondary"])
        dark_mode_frame.pack(fill="x", pady=10)
        
        dark_mode_label = tk.Label(dark_mode_frame, text="Dark Mode:", 
                                font=("Arial", 14, "bold"), bg=self.theme["bg_secondary"], fg=self.theme["text_primary"])
        dark_mode_label.pack(side="left", pady=5)
        
        self.dark_mode_var = tk.BooleanVar(value=self.is_dark_mode)
        dark_mode_check = tk.Checkbutton(dark_mode_frame, 
                                        variable=self.dark_mode_var,
                                        onvalue=True, offvalue=False,
                                        bg=self.theme["bg_secondary"], fg=self.theme["text_primary"],
                                        selectcolor=self.theme["bg_secondary"],
                                        command=self.preview_theme_change)
        dark_mode_check.pack(side="left", padx=10)
        
        # Add a visual indicator
        self.dark_mode_indicator = tk.Canvas(dark_mode_frame, width=30, height=15, bg=self.theme["bg_secondary"], 
                                           highlightthickness=0)
        self.dark_mode_indicator.pack(side="left", padx=5)
        self.update_dark_mode_indicator()
        
        # Color picker section with improved layout
        color_label = tk.Label(theme_container, text="Accent Color:", 
                          font=("Arial", 14, "bold"), bg=self.theme["bg_secondary"], fg=self.theme["text_primary"])
        color_label.pack(anchor="w", pady=(20, 10))
        
        # Color sample - larger and more prominent
        self.color_sample = tk.Canvas(theme_container, width=200, height=40, bg=self.accent_color, highlightthickness=1, 
                                    highlightbackground=self.theme["text_secondary"])
        self.color_sample.pack(pady=10)
        
        # Predefined colors in a grid layout
        presets_frame = tk.Frame(theme_container, bg=self.theme["bg_secondary"])
        presets_frame.pack(fill="x", pady=20)
        
        presets_label = tk.Label(presets_frame, text="Preset Colors:", 
                           font=("Arial", 12, "bold"), bg=self.theme["bg_secondary"], fg=self.theme["text_primary"])
        presets_label.pack(anchor="w")
        
        colors_frame = tk.Frame(presets_frame, bg=self.theme["bg_secondary"])
        colors_frame.pack(pady=10)
        
        preset_colors = [
            "#2A7FFF",  # Blue
            "#FF5722",  # Deep Orange
            "#4CAF50",  # Green
            "#9C27B0",  # Purple
            "#F44336",  # Red
            "#009688",  # Teal
            "#FFC107",  # Amber
            "#795548"   # Brown
        ]
        
        # Create a grid of color squares
        for i, color in enumerate(preset_colors):
            color_btn = tk.Button(colors_frame, bg=color, width=3, height=1, 
                              command=lambda c=color: self.change_theme_color(c))
            color_btn.grid(row=i//4, column=i%4, padx=5, pady=5)
        
        # Custom color button with improved styling
        custom_btn = tk.Button(theme_container, text="Choose Custom Color", 
                         command=self.choose_custom_color,
                         font=("Arial", 12),
                         bg=self.accent_color, fg=self.theme["text_inverse"])
        custom_btn.pack(pady=20)
        
        # Buttons container for better spacing
        button_container = tk.Frame(theme_container, bg=self.theme["bg_secondary"])
        button_container.pack(fill="x", pady=10)
        
        # Apply button with modern styling
        apply_btn = tk.Button(button_container, text="Apply Theme", 
                        command=self.apply_theme,
                        font=("Arial", 14, "bold"),
                        bg=self.accent_color, fg=self.theme["text_inverse"],
                        padx=20, pady=10)
        apply_btn.pack(side="left", padx=(0, 10))
        
        # Reset button with better contrast
        reset_btn = tk.Button(button_container, text="Reset to Default", 
                        command=self.reset_theme,
                        font=("Arial", 12),
                        bg=self.theme["bg_secondary"], fg=self.theme["text_primary"],
                        padx=10, pady=5)
        reset_btn.pack(side="left")
    
    def update_dark_mode_indicator(self):
        """Update the visual indicator for dark mode"""
        self.dark_mode_indicator.delete("all")
        if self.dark_mode_var.get():
            # Dark mode - draw moon icon
            self.dark_mode_indicator.create_oval(5, 3, 15, 13, fill="#E8E8E8", outline="")
            self.dark_mode_indicator.create_oval(8, 2, 18, 12, fill=self.theme["bg_secondary"], outline="")
        else:
            # Light mode - draw sun icon
            self.dark_mode_indicator.create_oval(8, 2, 18, 12, fill="#FFC107", outline="")
            
    def preview_theme_change(self):
        """Preview dark/light mode changes without fully applying theme"""
        self.is_dark_mode = self.dark_mode_var.get()
        if self.is_dark_mode:
            self.theme = self.dark_theme.copy()
        else:
            self.theme = self.light_theme.copy()
        
        # Update just the theme settings screen
        for widget in self.root.grid_slaves(row=0, column=1):
            self.update_widget_colors(widget)
            
        self.update_dark_mode_indicator()
    
    def choose_custom_color(self):
        color = colorchooser.askcolor(initialcolor=self.accent_color)
        if color[1]:  # If color is chosen (not cancelled)
            self.change_theme_color(color[1])
    
    def change_theme_color(self, color):
        self.accent_color = color
        self.color_sample.config(bg=color)
    
    def apply_theme(self):
        # Update settings with current theme
        self.settings["accent_color"] = self.accent_color
        self.settings["dark_mode"] = self.is_dark_mode
        
        # Update color variables based on theme
        if self.is_dark_mode:
            self.theme = self.dark_theme.copy()
        else:
            self.theme = self.light_theme.copy()
            
        self.save_settings()
        
        # Apply to root
        self.root.configure(bg=self.theme["bg_primary"])
        
        # Apply to all widgets
        self.update_widget_colors(self.root)
        
        # Force a restart of the current screen to apply all changes correctly
        current_screen = self.root.grid_slaves(row=0, column=1)
        if current_screen:
            # Store which screen we're on
            if hasattr(current_screen[0], '_name'):
                current_screen_name = current_screen[0]._name
                if 'theme' in current_screen_name:
                    self.show_theme_settings()
                elif 'essay' in current_screen_name:
                    self.show_essay_writer()
                elif 'study' in current_screen_name:
                    self.show_study_buddy()
                elif 'timer' in current_screen_name:
                    self.show_study_timer()
                elif 'todo' in current_screen_name:
                    self.show_todo_list()
                else:
                    self.show_dashboard()
            else:
                # If we can't determine the screen, just go to dashboard
                self.show_dashboard()
        else:
            # If no screen detected, go to dashboard
            self.show_dashboard()
        
        # Show success message
        messagebox.showinfo("Theme Applied", "Theme settings have been applied successfully!")

    def update_widget_colors(self, parent):
        """Recursively update all widget colors based on current theme"""
        for widget in parent.winfo_children():
            try:
                # Update based on widget type
                if isinstance(widget, tk.Frame) or isinstance(widget, ttk.Frame):
                    widget.configure(bg=self.theme["bg_primary"])
                    
                elif isinstance(widget, tk.LabelFrame):
                    widget.configure(bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
                    
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=self.theme["bg_primary"], fg=self.theme["text_primary"])
                    # Special handling for headings
                    if "bold" in str(widget["font"]):
                        # Only set accent color for headings that are direct children of frames
                        if widget.winfo_parent() and ("frame" in widget.winfo_parent().lower() or widget.winfo_parent().endswith("!frame")):
                            if "!labelframe" not in widget.winfo_parent().lower():  # Don't override LabelFrame titles
                                widget.configure(fg=self.accent_color)
                        
                elif isinstance(widget, tk.Button):
                    # Check if it's an accent button or regular button
                    if widget["bg"] == self.accent_color or widget["bg"] == "#FF5722" or widget["bg"] == "#4CAF50":
                        # Keep accent buttons with their colors
                        widget.configure(fg=self.theme["text_inverse"])
                    else:
                        # Regular buttons get theme colors
                        widget.configure(bg=self.theme["bg_secondary"], fg=self.theme["text_primary"])
                        
                elif isinstance(widget, tk.Entry) or isinstance(widget, tk.Spinbox):
                    widget.configure(bg=self.theme["input_bg"], fg=self.theme["input_text"],
                                    insertbackground=self.theme["text_primary"])
                    
                elif isinstance(widget, tk.Text):
                    widget.configure(bg=self.theme["input_bg"], fg=self.theme["input_text"],
                                    insertbackground=self.theme["text_primary"])
                    
                    # Special configuration for chat history and session logs
                    if "chat_history" in str(widget) or "session_log" in str(widget):
                        if self.is_dark_mode:
                            widget.tag_configure("sender", foreground="#7ADBFC")  # Light blue
                            widget.tag_configure("message", foreground="#E8E8E8")  # Light text
                            widget.tag_configure("heading", foreground="#7ADBFC")  # Light blue
                            widget.tag_configure("timestamp", foreground="#BBBBBB")  # Gray text
                        else:
                            widget.tag_configure("sender", foreground="#0066CC")  # Dark blue
                            widget.tag_configure("message", foreground="#333333")  # Dark text
                            widget.tag_configure("heading", foreground="#0066CC")  # Dark blue
                            widget.tag_configure("timestamp", foreground="#666666")  # Gray text
                    
                elif isinstance(widget, tk.Checkbutton) or isinstance(widget, tk.Radiobutton):
                    widget.configure(bg=self.theme["bg_primary"], fg=self.theme["text_primary"],
                                   selectcolor=self.theme["bg_secondary"])
                    
                elif isinstance(widget, tk.Canvas):
                    widget.configure(bg=self.theme["bg_primary"])
                    
                elif isinstance(widget, tk.Listbox):
                    widget.configure(bg=self.theme["input_bg"], fg=self.theme["input_text"],
                                    selectbackground=self.accent_color, selectforeground=self.theme["text_inverse"])
                    
                # Handle ttk widgets by updating the style
                elif isinstance(widget, ttk.Treeview):
                    style = ttk.Style()
                    style.configure("Treeview", 
                                    background=self.theme["input_bg"], 
                                    foreground=self.theme["input_text"],
                                    fieldbackground=self.theme["input_bg"])
                    style.map('Treeview', 
                            background=[('selected', self.accent_color)],
                            foreground=[('selected', self.theme["text_inverse"])])
                    
                # Recursively update any children
                self.update_widget_colors(widget)
                
            except Exception as e:
                # Skip widgets that can't be configured
                continue
    
    def reset_theme(self):
        self.change_theme_color("#2A7FFF")
        self.is_dark_mode = False
        self.theme = self.light_theme.copy()
        self.settings["dark_mode"] = False
        self.save_settings()
        self.show_dashboard()
    
    def show_calculator(self):
        # Clear main content area
        for widget in self.root.grid_slaves(row=0, column=1):
            if widget:
                widget.destroy()

        # Create a frame for the calculator
        calculator_frame = tk.Frame(self.root, bg=self.theme["bg_primary"], padx=20, pady=20)
        calculator_frame.grid(row=0, column=1, sticky="nsew")

        # Title
        title = tk.Label(calculator_frame, text="Calculator", 
                       font=("Arial", 16, "bold"), bg=self.theme["bg_primary"], fg=self.accent_color)
        title.pack(pady=10)

        # Entry field
        entry_frame = tk.Frame(calculator_frame, bg=self.theme["bg_primary"])
        entry_frame.pack(pady=10)

        self.calc_entry = tk.Entry(entry_frame, font=('Arial', 16), width=30,
                                 bg=self.theme["input_bg"], fg=self.theme["input_text"])
        self.calc_entry.pack(side="left")

        # Button frame
        button_frame = tk.Frame(calculator_frame, bg=self.theme["bg_primary"])
        button_frame.pack(pady=10)

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3)
        ]

        for (text, row, col) in buttons:
            tk.Button(button_frame, text=text, width=5,
                      command=lambda t=text: self.calc_button_click(t)) \
                .grid(row=row, column=col, padx=2, pady=2)

    def calc_button_click(self, text):
        if text == '=':
            try:
                result = eval(self.calc_entry.get())
                self.calc_entry.delete(0, tk.END)
                self.calc_entry.insert(0, str(result))
            except Exception as e:
                self.calc_entry.delete(0, tk.END)
                self.calc_entry.insert(0, "Error")
        else:
            self.calc_entry.insert(tk.END, text)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EduPal()
    app.run()
