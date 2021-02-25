# ece574
network security

1. Unencrypted File Transfer (uft)
In Part 1, you will use network sockets to transfer a file between hosts. To simplify operation, the client will read a file from STDIN and the server will “save” the file to STDOUT. Your code for the client and server must reside in the same Python script (uft), which must conform to the following command line options:

uft [-l PORT] [DESTINATION PORT] 
For example, the following is an example execution.

[client]$ ./uft server.add.ress 9999 < some-file.txt

[server]$ ./uft -l 9999 > some-file.txt
Both programs must terminate after the file is sent. You may assume the server is started before the client.

Important: All parts of this assignment must work for both small and big files, both text based and binary based. I recommend trying first with a simple text file and then testing with a PDF before submitting.

Tip: I recommend using a fixed size “header” containing the size of the message being sent. While it may not be needed for Part 1, it will be useful for Part 2 when you need to read a full message before decrypting. Debugging this in Part 1 will simplify your effort on Part 2.

2. Encrypted File Transfer (eft)
In Part 2, you will extend uft with symmetric encryption and integrity verification using AES and the Galios Counter Mode (AES-GCM) mode of operation. Recall that GCM avoides the need to incorporate integrity into the cryptographic protocol (e.g., Encrypt-then-MAC).

To perform the encryption, you will use PyCryptodome. Note that PyCryptodome is a drop-in replacement for PyCrypto, which does not support GCM. Unfortunately, most systems provide PyCrypto instead of PyCryptodome, so you may need to read the installation instructions. The documentation for PyCryptodome has several useful examples, but you will likely need to read the API documentation, specifically for using GCM.

You must:

Use AES-256 in GCM mode
Compute the key from the command line argument using PBKDF2 (Password-Based Key Derivation Function), which is available in PyCryptodome. Note that that using PBKDF2 requires a salt, which is a securely generated random value. Both the client and server need to use the same salt; therefore, your connection should start with the client sending the salt to the server. This initial exchange will also get you ready for Part 3.
To successfully decrypt the data, the server must receive the IV (“nonce” in the GCM API) from the client.
Your code for the client and server must reside in the same Python script (eft), which must conform to the following command line options:

eft -k KEY [-l PORT] [DESTINATION PORT] 
For example, the following is an example execution.

[client]$ ./eft -k SECURITYISAWESOME server.add.ress 9999 < some-file.txt

[server]$ ./eft -k SECURITYISAWESOME -l 9999 > some-file.txt
If an integrity error occurs (e.g., the key incorrect), the server should write an ERROR to STDERR as follows. You may assume the server is started before the client.

[client]$ ./eft -k SECURITYISAWESOME server.add.ress 9999 < some-file.txt

[server]$ ./eft -k SECURITYISBORING -l 9999 > some-file.txt
Error: integrity check failed.
Note that this exact error message is required to pass automated grading checks.

3. Encrypted File Transfer with Diffie-Hellman Key Exchange (eft-dh)
In Part 3, you will extend eft to calcuate a key using the Diffie-Hellman key exchange protocol. Therefore, instead of getting the key from the command line, you will first perform a DH message exchange between the client and the server to establish a symmetric key.

For the key exchange, we will use a fixed g and p as follows:

g=2
p=0x00cc81ea8157352a9e9a318aac4e33ffba80fc8da3373fb44895109e4c3ff6cedcc55c02228fccbd551a504feb4346d2aef47053311ceaba95f6c540b967b9409e9f0502e598cfc71327c5a455e2e807bede1e0b7d23fbea054b951ca964eaecae7ba842ba1fc6818c453bf19eb9c5c86e723e69a210d4b72561cab97b3fb3060b
You must use a good, cryptographic source of randomenss for the DH secrets. Do not use Python’s random.random PyCryptodome has a secure random number generator. You may also use os.urandom() in Python.

Note that Python has native support for handling large numbers (e.g., pow() for exponentiation). If you are using C (not supported for the class), you will need libgmp.

Your code for the client and server must reside in the same Python script (eft-dh), which must conform to the following command line options:

eft-dh [-l PORT] [DESTINATION PORT] 
For example, the following is an example execution.

[client]$ ./eft-dh server.add.ress 9999 < some-file.txt

[server]$ ./eft-dh -l 9999 > some-file.txt
You may assume the server is started before the client.

4. Middle-Person Attack on DH Key Exchange (dh-proxy)
In Part 4, you will a create proxy called dh-proxy that performs a middle-person attack on eft-dh. To simplify the assignment, we will assume the client connects directly to the proxy and that the proxy connects directly to the target server. Recall from class that a middle-person attack is achieved by a) establishing a DH exchange with the client; b) establishing a DH exchange with the server; and c) decrypting data from the client and re-encrypting data to the server. Therefore, you will be able to reuse your DH key exchange code from Part 3.

The tricky part of this part is not the crypto, but rather the network programming. You need to read from the socket with the client and then write to the socket for the server. While you could use threads to handle this, select is much easier to use.

You must conform to the following command line options:

dh-proxy -l PORT TARGET PORT
For example, the following is an example execution

[client]$ ./eft-dh proxy.add.ress 9999 < some-file.txt

[proxy]$  ./dh-proxy -l 9999 server.add.ress 9999

[server]$ ./eft-dh -l 9999 > some-file.txt
You may assume the server is started first, then the proxy, then the client.

Part 5 (10 Extra Credit Points): Logjam attack on DH Key Exchange (lj-proxy)
Part 5 is strictly optional extra credit. I have not completed it, and I don’t know how easy or hard it is. However, the idea is to use the logjam attack to eavesdrop on the communication between the client and server without performing multiple DH key exchanges. Instead, you should brute force the established key via the logjam attack and write the contents of the transmitted file to STDOUT.

You must conform to the following command line options:

lj-proxy -l PORT TARGET PORT
For example, the following is an example execution.

[client]$ ./eft-dh proxy.add.ress 9999 < some-file.txt

[proxy]$  ./lj-proxy -l 9999 server.add.ress 9999 > some-file.txt

[server]$ ./eft-dh -l 9999 > some-file.txt
You may assume the server is started first, then the proxy, then the client.

Note that since this may be beyond the computational ability of your personal computer, you may modify the g and p used in eft-dh. In this case, provide an alternate eft-dh-weak file that has this change. The solution with the largest p will receive and additional 5 points.

CSC/ECE 574 - Computer and Network Security
CSC/ECE 574 - Computer and Network Security
whenck@ncsu.edu
This is the course website for the Spring 2021 offering of CSC/ECE 574, Computer and Network Security, at the North Carolina State University.
