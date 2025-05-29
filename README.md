<p align="center">
  <img src="https://github.com/FanoyG/vpc-builder/blob/main/assets/vpc-builder-high-resolution-logo.png" alt="vpc-builder Logo" width="400"/>
</p>
<p align="center">
  <!-- ⭐ GitHub Project Info -->
  <img src="https://img.shields.io/github/stars/FanoyG/vpc-builder?style=social" alt="GitHub Stars"/>
  <img src="https://img.shields.io/github/forks/FanoyG/vpc-builder?style=social" alt="GitHub Forks"/>
  <img src="https://img.shields.io/github/issues/FanoyG/vpc-builder?color=yellow" alt="GitHub Issues"/>
  <img src="https://img.shields.io/github/issues-pr/FanoyG/vpc-builder?color=blueviolet" alt="GitHub Pull Requests"/>
  <img src="https://img.shields.io/github/license/FanoyG/vpc-builder?color=brightgreen" alt="GitHub License"/>

  <!-- 🐍 Python & Platform -->
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version"/>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Supported Platforms"/>

  <!-- 🚀 Activity -->
  <img src="https://img.shields.io/github/last-commit/FanoyG/vpc-builder?color=blue" alt="Last Commit"/>
  <img src="https://img.shields.io/github/repo-size/FanoyG/vpc-builder?color=orange" alt="Repo Size"/>
  <img src="https://img.shields.io/github/contributors/FanoyG/vpc-builder?color=purple" alt="Contributors"/>

  <!-- 🌐 Community & Docs -->
  <img src="https://img.shields.io/badge/GitHub%20Codespaces-Open%20Now-blue?logo=github" alt="GitHub Codespaces"/>
  <img src="https://img.shields.io/badge/Docs-Available-brightgreen" alt="Docs Available"/>
  <img src="https://img.shields.io/badge/Made%20with-❤️-red" alt="Made with Love"/>
</p>

<h3 align="center"><em>Simplify and automate AWS VPC creation and management with a powerful Python CLI tool leveraging AWS CLI — designed for efficiency, scalability, and ease of use.</em></h3>



---
# 🌐 Overview

**vpc-builder** is a beginner-friendly yet powerful Python CLI tool that helps you create, access, modify, and delete AWS Virtual Private Clouds (VPCs) and their components with ease.

No need to touch the AWS Console or memorize CLI syntax — just follow the interactive prompts!

### ❓ Why Use vpc-builder?

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
    git clone https://github.com/FanoyG/vpc-builder.git
    cd vpc-builder
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
[📺 Watch the vpc-builder walkthrough on YouTube](https://www.youtube.com/watch?v=PLACEHOLDER_LINK)

---

## 🛠️ Troubleshooting & Community Support

- ✅ **Ensure AWS CLI is configured** (`aws configure`)
- ✅ **Confirm IAM role has VPC-related permissions**
- ✅ **Run from the root directory**
- 🤝 **Still stuck? [Open an issue](https://github.com/FanoyG/vpc-builder/issues)**

---

## 🧪 Tests (Planned)
  - We're working on unit and integration tests using `pytest`.  
  - Want to help? Check the `tests/` folder or [open an issue](https://github.com/FanoyG/vpc-builder/issues).

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

**Steps to Contribute (Command Line):**

> 1. **Fork this repo**  
>    Using GitHub CLI (recommended):  
>    ```
>    gh repo fork FanoyG/vpc-builder --clone
>    cd vpc-builder
>    ```
>    *Or manually fork on GitHub, then clone your fork:*  
>    ```
>    git clone https://github.com/<your-username>/vpc-builder.git
>    cd vpc-builder
>    ```

> 2. **Create a new branch**  
>    ```
>    git checkout -b my-feature-branch
>    ```

> 3. **Make your changes**  
>    *(Edit, add, or delete files as needed)*

> 4. **Submit a PR 🎉**  
>    ```
>    git add .
>    git commit -m "Describe your changes"
>    git push origin my-feature-branch
>    ```
>    Then, open a Pull Request on GitHub from your branch.


---

## 📜 License

This project is licensed under the <a href="https://github.com/FanoyG/vpc-builder/blob/main/LICENSE">MIT Licence.</a>


---

## 👤 Author

**FanoyG**  
[GitHub: FanoyG](https://github.com/FanoyG)  
India 🇮🇳 | Cloud Engineer | AWS Infra-as-Code Builder (Python + CLI)

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

Have a cool feature idea? [Open an issue](https://github.com/FanoyG/vpc-builder/issues) or submit a PR!

<p align="center"> Made with ❤️ by <strong>FanoyG</strong> <br/> Automation Enthusiast (Python) &#124; AWS Explorer &#124; Open Source Builder </p>
