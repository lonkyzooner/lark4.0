# LARK for UniHiker M10 - Simple Deployment

This is a simplified version of the LARK (Law Enforcement Assistance and Response Kit) application specifically designed for the UniHiker M10 device.

## Files Included

- `index.html` - The main application file with a voice-first interface
- `serve.py` - A simple Python HTTP server to serve the application
- `install.sh` - Installation script to set up LARK on the UniHiker

## Deployment Instructions

### 1. Transfer to UniHiker

Copy this entire directory to your UniHiker M10 device. You can use SCP, USB drive, or any other method:

```bash
scp -r unihiker-simple/ user@unihiker-ip:/home/user/lark
```

### 2. Install on UniHiker

On the UniHiker device, navigate to the directory and run the installation script:

```bash
cd lark
chmod +x install.sh
./install.sh
```

### 3. Run LARK

After installation, you can start LARK by:

1. Double-clicking the LARK icon on your desktop, or
2. Running the Python server directly:

```bash
python3 serve.py
```

### 4. Access LARK

Open a web browser on the UniHiker and navigate to:

```
http://localhost:8080
```

## Using LARK

- The interface shows different visual states: idle, listening, processing, responding, and error
- Use the buttons at the bottom to simulate different commands
- The application will use the browser's built-in speech synthesis for voice output
- Microphone status is shown in the top-right corner

## Troubleshooting

If you encounter any issues:

1. **Server won't start**: Make sure Python 3 is installed on the UniHiker
2. **Browser can't connect**: Verify the server is running and you're using the correct URL
3. **No audio**: Check your speaker connection and volume settings

## Support

For additional help, refer to the main LARK documentation or contact support.
