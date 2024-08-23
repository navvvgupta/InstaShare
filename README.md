<h1 align="center" id="title">InstaShare Decentralized P2P File Sharing Platofrm</h1>

<p id="description">InstaShare is a decentralized peer-to-peer (P2P) file-sharing platform inspired by the popular Local DC++ system. Designed to facilitate seamless data exchange within a local network InstaShare empowers users with a suite of robust features that streamline the process of sharing and managing files.</p>

  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Decentralized Network: InstaShare operates on a decentralized network ensuring that there is no single point of failure. Users can connect directly with one another to share files without relying on a central server.
*   Real-time Chat: The platform is equipped with an integrated chat feature that allows users to communicate with one another in real-time.
*   Multiple File Sharing: -Hub allows users to share multiple files simultaneously. Whether you're distributing large datasets or sharing media files the platform handles it with ease.
*   Download Management: -Hub includes advanced download management features such as the ability to pause and resume downloads. This ensures that even if a connection is interrupted the download can be resumed from where it left off without any data loss.
*   Multi-threading Support: To enhance performance -Hub leverages multi-threading enabling users to upload and download multiple files concurrently. This parallel processing capability significantly reduces the time required for large file transfers.
*   User-friendly CLI: -Hub is designed with a command-line interface (CLI) that is both powerful and easy to use. Users can quickly execute commands to share files monitor transfers and communicate with other peers.

<h2> Functions</h2>

Here're functions:

*   connect(): To connect to any client for file tranfer.
*   upload(): To upload file/folder from my local device to Public folder so that users can see which whiles are avaialble within a user.
*   list_public_folder(username): To list publically available folder of a user
*   search_by_file(file_name): TO see wether this file is available within network with any user.
*   list_all_user(): To list all online users in a network.

<h2>System Architecture:</h2>

<img src="https://res.cloudinary.com/dpme2cbhg/image/upload/v1723577487/qa04hwmhpc5s9qmj7uyw.jpg" width="800" height="500/">

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the repository:</p>

```
git clone https://github.com/yourusername/InstaShare.git
```

<p>2. Navigate to the project directory:</p>

```
cd InstaShare
```

<p>3. Install the required dependencies:</p>

```
pip install -r requirements.txt
```

<p>4. Run InstaShare</p>

```
python client/client.py
```
