# User Guide

## Table of Contents
1. [System Overview](#system-overview)
2. [Administrator Guide](#administrator-guide)
3. [Voter Guide](#voter-guide)
4. [Security Features](#security-features)
5. [Troubleshooting](#troubleshooting)
6. [FAQ](#faq)

## System Overview

The Decentralized Online Voting System provides a secure, transparent, and accessible platform for conducting elections. The system supports three main user roles:

- **Administrators**: Manage elections, candidates, and voters
- **Voters**: Participate in elections through secure authentication
- **System**: Automated blockchain validation and result processing

## Administrator Guide

### 1. Administrator Dashboard

#### Accessing the Dashboard
1. Navigate to `http://localhost:8000/admin`
2. Enter your administrator credentials
3. You will be redirected to the main dashboard

#### Dashboard Features
- **Election Overview**: Active, upcoming, and completed elections
- **Voter Statistics**: Registration status and participation rates
- **Real-time Monitoring**: Live voting progress and results
- **System Health**: Database and blockchain status

### 2. Election Management

#### Creating a New Election

1. **Navigate to Election Creation**
   - Click "Create Election" from the dashboard
   - Or access via `/admin/create-election/`

2. **Fill Election Details**
   ```
   Election Name: General Election 2024
   Election Head: Chief Election Commissioner
   Election Date: 2024-05-15
   Constituency: North District
   Area: Urban and Rural Areas
   Address: Election Commission Office
   State: California
   City: Sacramento
   ZIP: 94214
   ```

3. **Upload Election Image**
   - Click "Choose File" to upload election banner
   - Supported formats: JPG, PNG, GIF
   - Maximum size: 5MB

4. **Set Election Parameters**
   - Voting start time
   - Voting end time
   - Eligibility criteria
   - Security settings

5. **Save and Publish**
   - Review all details
   - Click "Create Election"
   - Election is now active for voter registration

#### Managing Existing Elections

**View Elections**
- List view shows all elections with status
- Filter by date, status, or constituency
- Search by election name

**Edit Election**
- Click "Edit" next to any election
- Modify details as needed
- Changes are saved immediately

**Delete Election**
- Click "Delete" next to any election
- Confirm deletion in popup
- **Warning**: This action cannot be undone

### 3. Candidate Management

#### Adding Candidates

1. **Select Election**
   - Choose the election from the dropdown
   - Only active elections appear

2. **Enter Candidate Information**
   ```
   Candidate Name: John Smith
   Party Name: Progressive Party
   Party Symbol: [Upload image]
   ```

3. **Upload Party Symbol**
   - Recommended size: 200x200 pixels
   - Transparent background preferred
   - Formats: PNG, JPG, SVG

4. **Verify Information**
   - Review all details
   - Click "Add Candidate"

#### Managing Candidates

**View Candidate List**
- Shows all candidates for selected election
- Displays current vote counts
- Status indicators (Active, Inactive)

**Edit Candidate**
- Update candidate information
- Change party details
- Upload new symbols

**Remove Candidate**
- Remove from election
- Votes are preserved in audit trail

### 4. Voter Management

#### Voter Registration

1. **Manual Registration**
   - Click "Register Voter"
   - Enter voter details:
     ```
     Full Name: Jane Doe
     Aadhar Number: 1234-5678-9012
     Voter ID: VOT123456789
     Phone Number: +1-555-0123
     Email: jane.doe@email.com
     ```

2. **Bulk Registration**
   - Upload CSV file with voter details
   - Format: Name, Aadhar, Voter ID, Phone, Email
   - Maximum 1000 voters per file

3. **Verification Process**
   - System validates Aadhar and Voter ID
   - Sends OTP to registered phone
   - Status updates to "Pending Verification"

#### Voter Status Management

**Status Types**
- **Pending**: Initial registration
- **Verified**: Documents validated
- **Active**: Eligible to vote
- **Voted**: Has cast vote
- **Suspended**: Temporarily blocked

**Actions Available**
- Approve pending registrations
- Suspend suspicious accounts
- Reactivate suspended voters
- Export voter lists

### 5. Election Monitoring

#### Real-time Dashboard

**Live Statistics**
- Total registered voters
- Voters who have cast votes
- Voting percentage by constituency
- Leading candidates

**Security Monitoring**
- Failed authentication attempts
- Suspicious voting patterns
- Blockchain validation status
- System performance metrics

#### Results Management

**View Results**
- Live vote counting
- Candidate-wise results
- Constituency-wise breakdown
- Historical comparisons

**Publish Results**
- Mark election as complete
- Generate official results
- Export to PDF/Excel
- Publish to public portal

## Voter Guide

### 1. Registration Process

#### Initial Registration

1. **Access Registration Portal**
   - Navigate to `http://localhost:8000/voter/register`
   - Click "New Voter Registration"

2. **Enter Personal Information**
   ```
   Full Name: Jane Doe
   Date of Birth: 1990-01-15
   Gender: Female
   Address: 123 Main St, Sacramento, CA 94214
   ```

3. **Provide Identification**
   - Aadhar Card Number: 1234-5678-9012
   - Voter ID Number: VOT123456789
   - Phone Number: +1-555-0123
   - Email Address: jane.doe@email.com

4. **Upload Documents**
   - Aadhar card scan (PDF/JPG)
   - Voter ID card scan
   - Passport size photograph

5. **Submit Registration**
   - Review all information
   - Accept terms and conditions
   - Click "Submit Registration"

#### Verification Process

1. **Document Verification**
   - System validates uploaded documents
   - Cross-checks with government databases
   - Status updates via email/SMS

2. **Mobile Verification**
   - OTP sent to registered phone
   - Enter 6-digit OTP within 10 minutes
   - Maximum 3 attempts allowed

3. **Biometric Enrollment**
   - Schedule biometric capture appointment
   - Visit designated verification center
   - Face scan and fingerprint capture

### 2. Voting Process

#### Pre-Voting Preparation

1. **Check Eligibility**
   - Log in to voter portal
   - Verify registration status
   - Check upcoming elections

2. **System Requirements**
   - Modern web browser (Chrome, Firefox, Safari)
   - Stable internet connection
   - Webcam for face verification
   - Fingerprint scanner (if available)

#### Authentication Process

1. **Login to Voting Portal**
   - Navigate to `http://localhost:8000/voter/login`
   - Enter Aadhar number and password
   - Click "Login"

2. **Multi-Factor Authentication**
   
   **Step 1: OTP Verification**
   - OTP sent to registered phone
   - Enter 6-digit OTP
   - Auto-submit after correct entry

   **Step 2: Face Recognition**
   - Allow camera access
   - Position face in frame
   - System matches with enrolled data
   - Takes 5-10 seconds

   **Step 3: Fingerprint Verification** (Optional)
   - Connect fingerprint scanner
   - Place finger on scanner
   - System validates fingerprint
   - Provides additional security layer

3. **Security Check**
   - System validates all authentication factors
   - Checks for suspicious activity
   - Grants access to voting interface

#### Casting Your Vote

1. **Select Election**
   - List of available elections appears
   - Click "Vote" for desired election
   - Review election details

2. **Review Candidates**
   - Candidate list with photos
   - Party symbols and names
   - Click candidate for details
   - Compare candidate profiles

3. **Cast Vote**
   - Select preferred candidate
   - Click "Confirm Selection"
   - Review choice in confirmation screen
   - Click "Cast Vote"

4. **Blockchain Confirmation**
   - Vote encrypted using blockchain
   - Unique transaction ID generated
   - Confirmation screen displays:
     ```
     Vote Successfully Cast!
     Transaction ID: 0x7f9a2b3c4d5e6f...
     Timestamp: 2024-05-15 14:30:25 UTC
     Verification Hash: a1b2c3d4e5f6...
     ```

5. **Vote Receipt**
   - Download PDF receipt
   - Email confirmation sent
   - SMS notification with transaction ID

### 3. Vote Tracking

#### Check Vote Status

1. **Access Vote Tracking**
   - Log in to voter portal
   - Navigate to "My Votes"
   - View voting history

2. **Vote Details**
   - Election participated
   - Date and time of vote
   - Transaction ID
   - Blockchain verification status

#### Verify Vote Integrity

1. **Blockchain Verification**
   - Enter transaction ID
   - System retrieves vote from blockchain
   - Confirms vote integrity

2. **Audit Trail**
   - Complete voting history
   - Authentication logs
   - System access records

## Security Features

### 1. Multi-Factor Authentication

#### Aadhar Integration
- Government-issued identity verification
- Real-time validation with UIDAI database
- Biometric data matching

#### Biometric Verification
- Face recognition using AI algorithms
- Fingerprint matching with enrolled templates
- Liveness detection to prevent spoofing

#### OTP Security
- Time-based one-time passwords
- SMS delivery with encryption
- Rate limiting to prevent brute force

### 2. Blockchain Security

#### Vote Encryption
- SHA-256 hashing algorithm
- Immutable vote records
- Cryptographic signatures

#### Audit Trail
- Complete transaction history
- Tamper-evident logging
- Real-time integrity checks

#### Decentralization
- Distributed ledger technology
- No single point of failure
- Consensus-based validation

### 3. Data Protection

#### Encryption Standards
- AES-256 encryption for data at rest
- TLS 1.3 for data in transit
- End-to-end encryption for communications

#### Privacy Protection
- Personal data anonymization
- GDPR compliance
- Minimal data collection principle

#### Access Control
- Role-based permissions
- Session management
- Automatic logout after inactivity

## Troubleshooting

### Common Issues

#### Registration Problems

**Issue**: Aadhar validation failed
**Solution**: 
- Verify Aadhar number format (12 digits)
- Ensure Aadhar is linked to mobile number
- Check spelling and spaces

**Issue**: Document upload failed
**Solution**:
- Check file size (max 5MB)
- Verify file format (PDF, JPG, PNG)
- Ensure document is clear and readable

#### Authentication Issues

**Issue**: OTP not received
**Solution**:
- Check mobile number is correct
- Verify network connectivity
- Wait 2-3 minutes for delivery
- Request new OTP if needed

**Issue**: Face recognition failed
**Solution**:
- Ensure proper lighting
- Position face in camera frame
- Remove glasses or masks
- Try different camera angle

#### Voting Issues

**Issue**: Cannot access voting portal
**Solution**:
- Check registration status
- Verify election is active
- Clear browser cache and cookies
- Try different browser

**Issue**: Vote not recorded
**Solution**:
- Check blockchain confirmation
- Verify transaction ID
- Contact support if issue persists

### Error Messages

#### Registration Errors
- `AADHAR_INVALID`: Aadhar number format incorrect
- `DOCUMENT_TOO_LARGE`: File size exceeds 5MB limit
- `PHONE_EXISTS`: Phone number already registered

#### Authentication Errors
- `OTP_EXPIRED`: OTP has expired, request new one
- `FACE_NOT_MATCHED`: Face scan doesn't match records
- `ACCOUNT_LOCKED`: Too many failed attempts

#### Voting Errors
- `ELECTION_NOT_ACTIVE`: Election is not currently active
- `ALREADY_VOTED`: Vote already cast for this election
- `BLOCKCHAIN_ERROR`: Unable to record vote on blockchain

## FAQ

### General Questions

**Q: Is the voting system secure?**
A: Yes, the system uses military-grade encryption, blockchain technology, and multi-factor authentication to ensure maximum security.

**Q: Can I vote from anywhere?**
A: Yes, you can vote from any location with internet access, subject to eligibility requirements.

**Q: How is my privacy protected?**
A: All personal data is encrypted, and votes are anonymized. The system complies with data protection regulations.

### Registration Questions

**Q: What documents do I need for registration?**
A: You need a valid Aadhar card, voter ID, phone number, and email address.

**Q: How long does registration take?**
A: Registration typically takes 2-3 business days, including document verification.

**Q: Can I update my information after registration?**
A: Yes, you can update your information through the voter portal, subject to verification.

### Voting Questions

**Q: Can I change my vote after casting?**
A: No, once a vote is cast and recorded on the blockchain, it cannot be changed.

**Q: How do I know my vote was counted?**
A: You receive a transaction ID and can verify your vote on the blockchain.

**Q: What if I lose my voting credentials?**
A: Contact support immediately. They will help you recover your account securely.

### Technical Questions

**Q: What browsers are supported?**
A: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

**Q: Do I need special hardware?**
A: A webcam is required for face verification. Fingerprint scanner is optional but recommended.

**Q: Is internet required for voting?**
A: Yes, a stable internet connection is required for the voting process.

## Support

### Contact Information

**Technical Support**
- Email: techsupport@votingsystem.com
- Phone: 1-800-VOTE-HELP
- Hours: 24/7 during elections

**General Inquiries**
- Email: info@votingsystem.com
- Phone: 1-800-VOTE-INFO
- Hours: Monday-Friday, 9 AM - 6 PM

**Emergency Support**
- Hotline: 1-800-VOTE-911
- Available during active elections only

### Online Resources

- **Help Center**: [votingsystem.com/help](https://votingsystem.com/help)
- **Video Tutorials**: [votingsystem.com/tutorials](https://votingsystem.com/tutorials)
- **FAQ Database**: [votingsystem.com/faq](https://votingsystem.com/faq)
- **Community Forum**: [forum.votingsystem.com](https://forum.votingsystem.com)

### Report Issues

To report security issues or bugs:
- **Security**: security@votingsystem.com
- **Bug Reports**: bugs@votingsystem.com
- **Feature Requests**: features@votingsystem.com

---

**Important**: This guide is for informational purposes. Always follow official election guidelines and regulations in your jurisdiction.
