/**
 * Deploy script for LARK on UniHiker M10
 * 
 * This script prepares the LARK application for deployment to the UniHiker M10 device.
 * It builds the application with UniHiker-specific optimizations and creates a deployment package.
 * 
 * Run this script with: node scripts/deploy-unihiker.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const archiver = require('archiver');

// Configuration
const DIST_DIR = path.join(__dirname, '../dist');
const DEPLOY_DIR = path.join(__dirname, '../deploy');
const UNIHIKER_PACKAGE = path.join(DEPLOY_DIR, 'lark-unihiker.zip');

// Ensure the deploy directory exists
if (!fs.existsSync(DEPLOY_DIR)) {
  fs.mkdirSync(DEPLOY_DIR, { recursive: true });
}

// Build the application with UniHiker optimizations
console.log('🔨 Building LARK for UniHiker M10...');
try {
  // Add UniHiker flag to force UniHiker mode
  const indexPath = path.join(__dirname, '../index.html');
  let indexContent = fs.readFileSync(indexPath, 'utf8');
  
  // Only add the script tag if it doesn't already exist
  if (!indexContent.includes('window.FORCE_UNIHIKER = true')) {
    indexContent = indexContent.replace(
      '</head>',
      '<script>window.FORCE_UNIHIKER = true;</script></head>'
    );
    fs.writeFileSync(indexPath, indexContent, 'utf8');
    console.log('✅ Added UniHiker flag to index.html');
  }
  
  // Run the build command
  execSync('npm run build', { stdio: 'inherit' });
  console.log('✅ Build completed successfully');
  
  // Restore original index.html if we modified it
  if (indexContent !== fs.readFileSync(indexPath, 'utf8')) {
    fs.writeFileSync(indexPath, indexContent, 'utf8');
    console.log('✅ Restored original index.html');
  }
} catch (error) {
  console.error('❌ Build failed:', error);
  process.exit(1);
}

// Create a deployment package
console.log('📦 Creating deployment package...');
try {
  // Create a file to write to
  const output = fs.createWriteStream(UNIHIKER_PACKAGE);
  const archive = archiver('zip', {
    zlib: { level: 9 } // Maximum compression
  });
  
  // Listen for archive warnings
  archive.on('warning', (err) => {
    if (err.code === 'ENOENT') {
      console.warn('⚠️ Warning:', err);
    } else {
      throw err;
    }
  });
  
  // Handle archive errors
  archive.on('error', (err) => {
    throw err;
  });
  
  // Pipe archive data to the file
  archive.pipe(output);
  
  // Add the dist directory contents to the archive
  archive.directory(DIST_DIR, false);
  
  // Add a README file with deployment instructions
  const readmeContent = `# LARK for UniHiker M10

## Deployment Instructions

1. Extract this ZIP file to a directory on your computer
2. Connect to your UniHiker M10 via SSH or USB
3. Copy the extracted files to the UniHiker's web server directory
4. Access the application via the UniHiker's web browser

## Features

- Voice-activated interface with "Hey LARK" wake word
- Miranda rights reading in multiple languages
- Louisiana statute lookups
- Audio-based threat detection
- Tactical feedback

## Troubleshooting

If you encounter any issues:
- Check that the UniHiker has internet connectivity
- Ensure the device has sufficient storage space
- Verify that the web server is running correctly

For additional support, please contact the development team.
`;
  
  archive.append(readmeContent, { name: 'README.md' });
  
  // Add a startup script for the UniHiker
  const startupScript = `#!/bin/bash
# LARK UniHiker Startup Script

# Set the web server directory
WEB_DIR="/var/www/html"

# Copy LARK files to web server directory
echo "Copying LARK files to web server..."
cp -r ./* $WEB_DIR/

# Set appropriate permissions
chmod -R 755 $WEB_DIR

# Start the web server if not already running
if ! systemctl is-active --quiet nginx; then
  echo "Starting web server..."
  systemctl start nginx
fi

echo "LARK is now available at http://localhost"
echo "You can access it from the UniHiker's web browser"
`;
  
  archive.append(startupScript, { name: 'install.sh', mode: 0o755 });
  
  // Finalize the archive
  archive.finalize();
  
  output.on('close', () => {
    const sizeInMB = (archive.pointer() / 1024 / 1024).toFixed(2);
    console.log(`✅ Deployment package created: ${UNIHIKER_PACKAGE} (${sizeInMB} MB)`);
    console.log('');
    console.log('📱 To deploy to UniHiker M10:');
    console.log('1. Copy the deployment package to the UniHiker');
    console.log('2. Extract the package on the device');
    console.log('3. Run the install.sh script');
    console.log('4. Access LARK via the UniHiker web browser');
  });
} catch (error) {
  console.error('❌ Failed to create deployment package:', error);
  process.exit(1);
}
