from flask import Flask, request, render_template_string


# RC4 Implementation
class RC4:
    def __init__(self, key):
        self.key = [ord(k) for k in key]
        self.s = list(range(256))
        self.key_schedule()  # Apply Key Scheduling Algorithm (KSA)

    def key_schedule(self):
        """Key Scheduling Algorithm (KSA)"""
        j = 0
        for i in range(256):
            j = (j + self.s[i] + self.key[i % len(self.key)]) % 256
            self.s[i], self.s[j] = self.s[j], self.s[i]

    def pseudorandom_number_generator(self):
        """Pseudorandom Number Generator (PRNG)"""
        i = j = 0
        while True:
            i = (i + 1) % 256
            j = (j + self.s[i]) % 256
            self.s[i], self.s[j] = self.s[j], self.s[i]
            k = self.s[(self.s[i] + self.s[j]) % 256]
            yield k  # Generate a new random number (key stream byte)

    def process(self, data):
        """Encrypt or decrypt the data using the RC4 algorithm"""
        prng = self.pseudorandom_number_generator()
        result = []
        for char in data:
            k = next(prng)  # Get the next random byte from PRNG
            result.append(chr(ord(char) ^ k))  # XOR operation to encrypt/decrypt
        return "".join(result)



# RC5 Implementation (Simplified for Demo Purposes)
class RC5:
    def __init__(self, key, rounds=12):
        self.key = [ord(k) for k in key]
        self.rounds = rounds

    def encrypt(self, plaintext):
        return "".join(chr((ord(c) + sum(self.key)) % 256) for c in plaintext)

    def decrypt(self, ciphertext):
        return "".join(chr((ord(c) - sum(self.key)) % 256) for c in ciphertext)


# RC6 Implementation (Simplified for Demo Purposes)
class RC6:
    def __init__(self, key, rounds=20):
        self.key = [ord(k) for k in key]
        self.rounds = rounds

    def encrypt(self, plaintext):
        return "".join(chr((ord(c) + len(self.key)) % 256) for c in plaintext)

    def decrypt(self, ciphertext):
        return "".join(chr((ord(c) - len(self.key)) % 256) for c in ciphertext)


# Flask App
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def encryption_decryption():
    result = ""
    output_text = ""

    if request.method == "POST":
        action = request.form.get("action")  # Encrypt or Decrypt
        cipher_type = request.form.get("cipher")
        key = request.form.get("key")

        if not key:
            result = "Please provide a key."
        else:
            if action == "encrypt":
                plaintext = request.form.get("text")
                if not plaintext:
                    result = "Please provide plaintext to encrypt."
                else:
                    if cipher_type == "RC4":
                        rc4 = RC4(key)
                        output_text = rc4.process(plaintext)
                    elif cipher_type == "RC5":
                        rc5 = RC5(key)
                        output_text = rc5.encrypt(plaintext)
                    elif cipher_type == "RC6":
                        rc6 = RC6(key)
                        output_text = rc6.encrypt(plaintext)
                    else:
                        result = "Invalid cipher selected."
                        output_text = ""
                    if not result:
                        result = "Encryption successful."

            elif action == "decrypt":
                ciphertext = request.form.get("text")
                if not ciphertext:
                    result = "Please provide ciphertext to decrypt."
                else:
                    if cipher_type == "RC4":
                        rc4 = RC4(key)
                        output_text = rc4.process(ciphertext)
                    elif cipher_type == "RC5":
                        rc5 = RC5(key)
                        output_text = rc5.decrypt(ciphertext)
                    elif cipher_type == "RC6":
                        rc6 = RC6(key)
                        output_text = rc6.decrypt(ciphertext)
                    else:
                        result = "Invalid cipher selected."
                        output_text = ""
                    if not result:
                        result = "Decryption successful."

    return render_template_string(TEMPLATE, result=result, output_text=output_text)


# HTML Template
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Encrypt and Decrypt</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 20px; }
        h1 { color: #333; }
        form { margin-bottom: 20px; }
        label { font-weight: bold; }
        input, select, textarea { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
        input[type="submit"] { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        input[type="submit"]:hover { background-color: #45a049; }
        .result { margin-top: 20px; padding: 10px; background-color: #e7f3e7; border: 1px solid #d4e2d4; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Encrypt and Decrypt Text</h1>
    <form method="post">
        <label for="action">Action:</label>
        <select name="action" id="action" required>
            <option value="encrypt">Encrypt</option>
            <option value="decrypt">Decrypt</option>
        </select>

        <label for="cipher">Cipher:</label>
        <select name="cipher" id="cipher" required>
            <option value="RC4">RC4</option>
            <option value="RC5">RC5</option>
            <option value="RC6">RC6</option>
        </select>

        <label for="key">Key:</label>
        <input type="text" id="key" name="key" placeholder="Enter key" required>

        <label for="text">Text:</label>
        <textarea id="text" name="text" rows="4" placeholder="Enter text here" required></textarea>

        <input type="submit" value="Submit">
    </form>

    {% if result %}
    <div class="result">
        <p><strong>{{ result }}</strong></p>
        {% if output_text %}
        <p>Output: {{ output_text }}</p>
        {% endif %}
    </div>
    {% endif %}
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
