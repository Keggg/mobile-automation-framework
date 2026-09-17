# Mobile Test Automation Framework (Android / Python / Appium)

A scalable, production-grade **Data-Driven Test Automation Framework** built to cover end-to-end (E2E) regression flows for a complex mobile application (insurance and fintech domain). 

The framework is architected from scratch using modern automation practices, strictly isolating test logic, execution states, and dynamic test data.

## 🚀 Key Features & Architecture

* **Data-Driven Architecture:** Test cases are completely separated from execution logic. Test matrices and user roles (Applicant/Contender, Individual/Entity) are managed via configuration dictionaries, allowing seamless scalability without modifying the core test runner.
* **Appium 2.x Compliant:** Utilizes modern `UiAutomator2Options` instead of deprecated desired capabilities, ensuring strict compliance with up-to-date W3C WebDriver standards.
* **Contextual State & Session Management:** Implements a unified `Context` wrapper to securely propagate the active WebDriver instance, explicit wait objects, and dynamic run-time state flags across modules.
* **Custom Context-Driven Logging:** Built an internal logging engine utilizing Python's `@contextmanager`. Steps are automatically prefixed with the active user actor (`[Applicant]`, `[Contender]`) for pristine log readability.
* **Automated Failure Screenshots:** The reporting engine intercepts runtime exceptions, automatically captures device screenshots via the native driver layer, sanitizes step names, and maps assets dynamically to the created application number.
* **Dynamic Log Management:** Features a dynamic log lifecycle. Tests begin in a generic buffer and are programmatically renamed and re-routed on-the-fly once the application generates a unique system transaction ID.

## 📂 Project Structure

```text
├── main.py           # Main entry point: orchestrates the test suite execution loop
├── driver_setup.py   # Driver initialization, capabilities, and explicit wait configuration
├── run_test.py       # Master E2E execution engine and conditional flow orchestration
├── helpers.py        # Reusable business-logic blocks, native gestures, and system alert handlers
├── scenarios.py      # Test case configuration data matrices (DDT Data Layer)
├── participants.py   # Factory module: maps raw test configurations into typed OOP domain models
├── models.py         # Object-oriented domain data models and entities
├── logger.py         # Context managers, live streams, and automated screenshot hook on failure
└── logs/             # Generated test session execution logs
```

## 🛠️ Tech Stack

* **Language:** Python 3.13+
* **Automation Tool:** Appium Python Client
* **Driver Engine:** UiAutomator2 (Android)
* **Design Patterns:** Data-Driven Testing (DDT), Context/State Wrapper

## ⚙️ Local Setup & Execution

### Prerequisites
1. Enable **Developer Options** and turn on **USB Debugging** on your physical Android device.
2. Connect the Android device to your workstation via USB cable.
3. Verify the device is connected by running `adb devices` in your terminal.
4. Install **Node.js** and **Appium 2.x** (`npm install -g appium`).
5. Install the driver: `appium driver install uiautomator2`.

### Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com
cd europrotocol
pip install appium-python-client selenium
```

### Running Tests
1. Ensure your physical device is connected and unlocked.
2. Spin up the Appium server in your terminal:
   ```bash
   appium
   ```
3. Execute the test runner:
   ```bash
   python main.py
   ```

---
*Note: In compliance with Non-Disclosure Agreements (NDA), the commercial application binary (.apk) and production environment credentials have been omitted from this public showcase repository.*
