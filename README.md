<p align="center">
  <img src="images/Screenshot-2025-05-29-104820-pica.png" alt="VPC-Builder Logo" width="400"/>
</p>

<p align="center">
  <a href="https://github.com/Fanoy/VPC-Builder">
    <img src="https://img.shields.io/github/stars/Fanoy/VPC-Builder?style=social" alt="GitHub stars"/>
  </a>
  <a href="https://github.com/Fanoy/VPC-Builder/issues">
    <img src="https://img.shields.io/github/issues/Fanoy/VPC-Builder" alt="GitHub issues"/>
  </a>
  <a href="https://github.com/Fanoy/VPC-Builder/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Fanoy/VPC-Builder" alt="MIT License"/>
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version"/>
  </a>
</p>


# 🚀 VPC-Builder

*A Python CLI tool to simplify AWS VPC creation and management using Terraform principles.*



## 🌐 Overview

**VPC-Builder** is a beginner-friendly yet powerful Python CLI tool that helps you create, access, modify, and delete AWS Virtual Private Clouds (VPCs) and their components with ease.

No need to touch the AWS Console or memorize CLI syntax — just follow the interactive prompts!

### ❓ Why Use VPC-Builder?

- 🚫 No AWS Console or complex CLI needed  
- 👶 Beginner-friendly flow, great for learners  
- 🧱 Modular and clean Python codebase  
- 💡 Understand AWS VPCs by building them  
- ⚡ Fast and reliable CLI experience  

---

## 🔧 Tech Stack

- **Python 3.8+**
- **Libraries:** `rich`, `questionary`, `boto3`
- **AWS CLI**
- **Test Suite (Planned):** `pytest`

---

## 🎯 Features

- 🔍 **Access VPCs:** View Subnets, Route Tables, IGWs, and more  
- 🛠️ **Create VPCs:** CIDR block wizard, subnet setup, routing logic  
- 🧠 **Modify Components:** Dynamically update VPC configurations  
- ❌ **Delete Resources:** Remove entire VPCs or specific parts  
- 💡 **Error Handling:** Edge-case validations built in  
- 🌈 **Beautiful Interface:** Rich formatting and color-coded output  
- ⏳ **Coming Soon:** Peering, Flow Logs, CloudWatch Monitoring  

---

## 🖼️ Screenshots

| Access Flow | Create Flow |
|-------------|-------------|
| ![Access Flow](https://via.placeholder.com/400x200?text=Access+Flow+Demo) | ![Create Flow](https://via.placeholder.com/400x200?text=Create+Flow+Demo) |

> 💡 Replace these images with real terminal GIFs or screenshots using tools like [Peek](https://github.com/phw/peek) or [asciinema](https://asciinema.org/).

---

## 🗂️ Project Structure

```bash
vpc-builder/
├── cli/
│   ├── __init__.py
│   ├── main.py
│   ├── display.py
│   ├── prompts.py
│   ├── access.py
│   ├── create.py
│   ├── modify.py
│   ├── delete.py
│   └── helpers.py
├── utils/
│   ├── __init__.py
│   └── validation.py
├── tests/
│   ├── __init__.py
│   ├── test_prompts.py
│   ├── test_display.py
│   ├── test_create_flow.py
│   └── test_access_flow.py
├── requirements.txt
├── setup.py
└── README.md
```
## 🚀 Getting Started

1. **Clone the repository**
    ```
    git clone https://github.com/Fanoy/VPC-Builder.git
    cd VPC-Builder
    ```

2. **(Optional) Set up a virtual environment**
    ```
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Run the tool**
    ```
    python cli/main.py
    ```

---

## 🎬 Demo (Coming Soon)
[📺 Watch the VPC-Builder walkthrough on YouTube](https://www.youtube.com/watch?v=PLACEHOLDER_LINK)

---

## 🛠️ Troubleshooting & Community Support

- ✅ **Ensure AWS CLI is configured** (`aws configure`)
- ✅ **Confirm IAM role has VPC-related permissions**
- ✅ **Run from the root directory**
- 🤝 **Still stuck? [Open an issue](https://github.com/Fanoy/VPC-Builder/issues)**

---

## 🧪 Tests (Planned)

We're working on unit and integration tests using `pytest`.  
Want to help? Check the `tests/` folder or [open an issue](https://github.com/Fanoy/VPC-Builder/issues).

---

## 🧭 Roadmap

| Status | Feature                                   |
|:------:|:------------------------------------------|
| ✅     | Access / Create / Modify / Delete Flows   |
| 🟡     | Test Suite for CLI modules                |
| 🔜     | VPC Peering support                       |
| 🔜     | CloudWatch Monitoring integration         |
| 🔜     | VPC Flow Logging                          |
| 🔜     | GUI Dashboard (Visual Layer)              |

---

## 🤝 Contributing

We welcome all contributions!

- ✅ **Testers:** Help validate edge cases
- 🎨 **Designers:** Enhance UX and visual flow
- 🧑‍💻 **Frontend Developers:** Build the future GUI

**Steps to Contribute:**

> &nbsp;&nbsp;&nbsp;1. Fork this repo  
> &nbsp;&nbsp;&nbsp;2. Create a new branch  
> &nbsp;&nbsp;&nbsp;3. Make your changes  
> &nbsp;&nbsp;&nbsp;4. Submit a PR 🎉  



---

## 📜 License

This project is licensed under the MIT License.

---

## 👤 Author

**Fanoy**  
[GitHub: Fanoy](https://github.com/Fanoy)  
India 🇮🇳 | Python Developer | Cloud Enthusiast

> “When something is important enough, you do it even if the odds are not in your favor.” — Elon Musk

---

## ⚠️ Warning

This project is under active development.  
It is ideal for learning, testing, or personal projects — not yet recommended for production use.

If unsure, press `Ctrl + C` to safely exit the CLI anytime.

---

## 🔮 Future Implementations

- 🔁 **VPC Peering**
- 📊 **CloudWatch Integration**
- 📄 **Flow Logs**
- 🌐 **Enhanced Internet & NAT Gateway Logic**
- 🧪 **More Test Coverage**
- 🖥️ **GUI Dashboard (React/Tailwind-based)**

Have a cool feature idea? [Open an issue](https://github.com/Fanoy/VPC-Builder/issues) or submit a PR!

<p align="center"> Made with ❤️ by <strong>Fanoy</strong> <br/> Python Developer &#124; AWS Explorer &#124; Open Source Builder </p>
