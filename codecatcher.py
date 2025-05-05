import tkinter as tk
from tkinter import messagebox, scrolledtext
import google.generativeai as genai

# Gemini API setup
GEMINI_API_KEY = 'AIzaSyDK-HUZY-kkLZAW_yjuqeJYASUsC_QKGXw'
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 2048
    }
)

# Main question
question = {
    "code": """int main() {
    int n = 5;
    vector<int> data;
    data.reserve(n);  // Intent: create space for 5 elements

    for (int i = 0; i < n; ++i) {
        data[i] = i + 1;  // Trying to initialize values
    }

    int sum = 0;
    for (int i = 0; i < data.size(); ++i) {
        sum += data[i];
    }

    cout << "Sum = " << sum << endl;
    return 0;
}""",
    "fix": "0"
}

# Follow-up question
followupq = {
    "code": "how would you append the vector within the same loop so that it stores elements from 1 to 5?",
    "fix": "data.push_back(i+1)"
}

class CodeCatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeCatcher Debug Game")
        self.score = 0
        self.max_attempts = 5
        self.main_attempts = 0
        self.followup_attempts = 0
        self.current_stage = "main"

        self.build_widgets()
        self.load_main_question()

    def build_widgets(self):
        self.prompt_label = tk.Label(self.root, text="Debug this code:", font=("Arial", 12))
        self.prompt_label.pack()

        self.code_box = scrolledtext.ScrolledText(self.root, height=12, width=80, font=("Courier", 10))
        self.code_box.pack()
        self.code_box.configure(state='disabled')

        self.input_label = tk.Label(self.root, text="Your Answer or Question:")
        self.input_label.pack()

        self.user_input = tk.Entry(self.root, width=80)
        self.user_input.pack()

        self.submit_btn = tk.Button(self.root, text="Submit", command=self.handle_submit)
        self.submit_btn.pack(pady=10)

        self.feedback = tk.Label(self.root,text="",font=("Helvetica", 12, "italic"),fg="white",bg="black",wraplength=600,justify="left"
)

        self.feedback.pack()

    def generate_hint(self, student_input, original_code=None):
        base_context = (
            "You are a helpful C++ instructor assisting a student who is debugging or learning code. "
            "Provide helpful hints, clarify misconceptions, and guide them to think — but absolutely do NOT give the final code fix or full answer. "
            "Explain concepts clearly like a tutor. "
        )

        if original_code:
            prompt = (
                base_context +
                "\n\nHere is the original buggy code the student is working with:\n" +
                original_code +
                "\n\nHere is the student's question or misunderstanding:\n" +
                student_input
            )
        else:
            prompt = base_context + "\n\nStudent's question:\n" + student_input

        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"(Error generating hint: {str(e)})"


    def load_main_question(self):
        self.current_stage = "main"
        self.display_code(question["code"])
        self.feedback.config(text="")

    def load_followup_question(self):
        self.current_stage = "followup"
        self.display_code(followupq["code"])
        self.feedback.config(text="")

    def display_code(self, code):
        self.code_box.configure(state='normal')
        self.code_box.delete("1.0", tk.END)
        self.code_box.insert(tk.END, code)
        self.code_box.configure(state='disabled')

    def handle_submit(self):
        text = self.user_input.get().strip()
        self.user_input.delete(0, tk.END)

        if self.current_stage == "main":
            self.main_attempts += 1
            if text == question["fix"]:
                self.feedback.config(text="✅ Correct! Moving to follow-up...")
                self.score += (6 - self.main_attempts)
                self.root.after(2000, self.load_followup_question)
            elif self.main_attempts >= self.max_attempts:
                messagebox.showinfo("Game Over", "You did not solve the main question. Score: 0")
                self.root.quit()
            else:
                hint = self.generate_hint(text, question["code"])
                self.feedback.config(text="❌ Incorrect. Hint:\n" + hint)

        elif self.current_stage == "followup":
            self.followup_attempts += 1
            if text == followupq["fix"]:
                self.score += (6 - self.followup_attempts)
                messagebox.showinfo("Game Complete", f"🏁 Final Score: {self.score}")
                self.root.quit()
            elif self.followup_attempts >= self.max_attempts:
                messagebox.showinfo("Game Complete", f"Follow-up not solved. Final Score: {self.score}")
                self.root.quit()
            else:
                hint = self.generate_hint(text, followupq["code"])
                self.feedback.config(text="❌ Incorrect. Hint:\n" + hint)


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeCatcherApp(root)
    root.mainloop()
