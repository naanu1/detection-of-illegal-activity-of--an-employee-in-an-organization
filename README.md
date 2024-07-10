# Detection of Illegal Activity of an Employee in an Organization

## Project Overview
This project aims to detect illegal activities by insider employees within an organization. It utilizes deep learning algorithms to analyze network data and identify malicious actions, such as breaching privileged files or leaking sensitive information. The system employs honeypot and Intrusion Detection System (IDS) techniques to trap malicious users by providing misleading information while preserving the security of actual data.

## Technologies Used
- **Deep Learning Algorithms:** GRU, ANN
- **Frontend:** HTML, CSS
- **Backend:** Flask (Python)
- **Database:** Cloud-based storage with original and duplicate datasets
- **Networking Dataset:** Includes features such as Destination Port, Flow Duration, Total Fwd Packets, Total Backward Packets, etc.

## Project Structure
The project is organized into the following folders and files:

### Main Project Folder
- **client**
  - Contains client-side input Python code and sample attack Excel files.

- **clientFE**
  - Contains frontend files (HTML, CSS) and `client.py` file which has Flask code for employee signup, login, and storing information in the database or Excel file. It handles authentication and authorization.

- **server**
  - **server.py:** Contains Flask code for the honeypot trap, sending emails, and logging attacker information.
  - **attack.py:** Analyzes user requests to determine if they are malicious. It contains the trained model (`model.h5`), feature extraction (`features.pkl`), and scaler (`scaler.pkl`) files. It logs activities in an Excel file.
  - **dataset files:** Contains CSV files and IPython Notebook files used for data preprocessing, model selection, and model training.

## Workflow
1. **Data Collection and Preprocessing:**
   - Collect network data and preprocess it to remove any inconsistencies.
   - Extract relevant features from the dataset for model training.
   - Scale and transform the data to make it suitable for deep learning models.

2. **Model Training:**
   - Use the preprocessed dataset to train deep learning models (GRU and ANN).
   - Compare the performance of GRU and ANN models, and select the best-performing model (GRU in this case).
   - Save the trained model, feature extraction, and scaler files.

3. **Client-Side Application:**
   - Employees can sign up and log in through the client-side application.
   - Employee information is stored securely in the database or an Excel file.
   - Authentication and authorization mechanisms ensure only legitimate users can access the system.

4.  **Server-Side Application:**
   - The server-side application uses a honeypot and IDS to detect malicious activities.
   - When an insider attacker tries to access sensitive files, the system analyzes the request using the trained model.
   - If the request is identified as malicious, the system responds with misleading information from a duplicate database.
   - The system logs the attacker's details (IP address, type of attack, attempted file access) and notifies the company HR via email.

5. **Logging and Notification:**
   - All activities, including normal and malicious access attempts, are logged in an Excel file.
   - The system sends an email to the company HR with details of any detected malicious activity.

## Usage
1. **Clone the Repository:**
