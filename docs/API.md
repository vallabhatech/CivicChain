# API Documentation

## Overview

The Decentralized Online Voting System provides RESTful APIs for managing elections, voters, candidates, and voting operations. This documentation covers all available endpoints, authentication methods, and response formats.

## Base URL

```
Development: http://localhost:8000/api/v1/
Production: https://your-domain.com/api/v1/
```

## Authentication

### API Key Authentication
All API requests require authentication using API keys.

**Headers:**
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Obtaining API Key:**
1. Contact system administrator
2. Provide organization details
3. Receive API key via secure email
4. Include key in all requests

### Rate Limiting
- **Standard**: 100 requests per minute
- **Premium**: 1000 requests per minute
- **Enterprise**: Unlimited requests

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## Response Format

### Success Response
```json
{
    "success": true,
    "data": {
        // Response data
    },
    "message": "Operation completed successfully",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### Error Response
```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input parameters",
        "details": {
            "field": "email",
            "reason": "Invalid email format"
        }
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| AUTH_REQUIRED | Authentication required | 401 |
| AUTH_INVALID | Invalid API key | 401 |
| RATE_LIMIT_EXCEEDED | Rate limit exceeded | 429 |
| VALIDATION_ERROR | Input validation failed | 400 |
| NOT_FOUND | Resource not found | 404 |
| PERMISSION_DENIED | Insufficient permissions | 403 |
| SERVER_ERROR | Internal server error | 500 |

## Endpoints

### 1. Authentication Endpoints

#### Generate OTP
Generate one-time password for voter authentication.

**Endpoint:** `POST /auth/otp/generate`

**Request Body:**
```json
{
    "phone_number": "+1234567890",
    "aadhar_number": "123456789012"
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "otp_id": "otp_123456789",
        "expires_at": "2024-01-01T12:05:00Z"
    },
    "message": "OTP sent successfully"
}
```

#### Verify OTP
Verify one-time password for authentication.

**Endpoint:** `POST /auth/otp/verify`

**Request Body:**
```json
{
    "otp_id": "otp_123456789",
    "otp_code": "123456"
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "expires_in": 3600
    },
    "message": "Authentication successful"
}
```

#### Refresh Token
Refresh access token using refresh token.

**Endpoint:** `POST /auth/refresh`

**Request Body:**
```json
{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. Voter Management Endpoints

#### Register Voter
Register a new voter in the system.

**Endpoint:** `POST /voters/register`

**Request Body:**
```json
{
    "full_name": "John Doe",
    "aadhar_number": "123456789012",
    "voter_id": "VOT123456789",
    "phone_number": "+1234567890",
    "email": "john.doe@example.com",
    "date_of_birth": "1990-01-15",
    "address": {
        "street": "123 Main St",
        "city": "Sacramento",
        "state": "CA",
        "zip_code": "94214",
        "country": "USA"
    }
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "voter_id": "VOT123456789",
        "registration_id": "REG_123456789",
        "status": "pending_verification"
    },
    "message": "Voter registration submitted successfully"
}
```

#### Get Voter Details
Retrieve voter information by voter ID.

**Endpoint:** `GET /voters/{voter_id}`

**Response:**
```json
{
    "success": true,
    "data": {
        "voter_id": "VOT123456789",
        "full_name": "John Doe",
        "status": "active",
        "registration_date": "2024-01-01T12:00:00Z",
        "last_login": "2024-01-15T10:30:00Z",
        "voting_history": [
            {
                "election_id": "ELEC_001",
                "election_name": "General Election 2024",
                "voted_at": "2024-01-15T11:00:00Z",
                "transaction_id": "0x7f9a2b3c4d5e6f..."
            }
        ]
    }
}
```

#### Update Voter Information
Update voter personal information.

**Endpoint:** `PUT /voters/{voter_id}`

**Request Body:**
```json
{
    "phone_number": "+1234567891",
    "email": "john.doe.new@example.com",
    "address": {
        "street": "456 Oak Ave",
        "city": "Los Angeles",
        "state": "CA",
        "zip_code": "90210"
    }
}
```

#### Get Voter Status
Check voter eligibility and status.

**Endpoint:** `GET /voters/{voter_id}/status`

**Response:**
```json
{
    "success": true,
    "data": {
        "voter_id": "VOT123456789",
        "status": "active",
        "eligible_elections": [
            {
                "election_id": "ELEC_001",
                "election_name": "General Election 2024",
                "voting_start": "2024-05-15T08:00:00Z",
                "voting_end": "2024-05-15T20:00:00Z"
            }
        ],
        "has_voted": false
    }
}
```

### 3. Election Management Endpoints

#### Create Election
Create a new election.

**Endpoint:** `POST /elections`

**Request Body:**
```json
{
    "election_name": "General Election 2024",
    "election_head": "Chief Election Commissioner",
    "election_date": "2024-05-15",
    "constituency": "North District",
    "area": "Urban and Rural Areas",
    "address": "Election Commission Office",
    "state": "California",
    "city": "Sacramento",
    "zip_code": "94214",
    "voting_start_time": "2024-05-15T08:00:00Z",
    "voting_end_time": "2024-05-15T20:00:00Z"
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "election_id": "ELEC_001",
        "status": "draft",
        "created_at": "2024-01-01T12:00:00Z"
    },
    "message": "Election created successfully"
}
```

#### Get Election List
Retrieve list of all elections.

**Endpoint:** `GET /elections`

**Query Parameters:**
- `status`: Filter by status (draft, active, completed)
- `limit`: Number of results per page (default: 20)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
    "success": true,
    "data": {
        "elections": [
            {
                "election_id": "ELEC_001",
                "election_name": "General Election 2024",
                "status": "active",
                "election_date": "2024-05-15",
                "total_voters": 100000,
                "votes_cast": 45000,
                "voting_percentage": 45.0
            }
        ],
        "pagination": {
            "total": 1,
            "limit": 20,
            "offset": 0,
            "has_next": false
        }
    }
}
```

#### Get Election Details
Retrieve detailed information about a specific election.

**Endpoint:** `GET /elections/{election_id}`

**Response:**
```json
{
    "success": true,
    "data": {
        "election_id": "ELEC_001",
        "election_name": "General Election 2024",
        "status": "active",
        "election_date": "2024-05-15",
        "voting_start_time": "2024-05-15T08:00:00Z",
        "voting_end_time": "2024-05-15T20:00:00Z",
        "constituency": "North District",
        "candidates": [
            {
                "candidate_id": "CAND_001",
                "candidate_name": "John Smith",
                "party_name": "Progressive Party",
                "votes": 25000
            }
        ],
        "statistics": {
            "total_voters": 100000,
            "votes_cast": 45000,
            "voting_percentage": 45.0
        }
    }
}
```

#### Update Election
Update election details.

**Endpoint:** `PUT /elections/{election_id}`

**Request Body:**
```json
{
    "election_name": "Updated General Election 2024",
    "voting_end_time": "2024-05-15T22:00:00Z"
}
```

### 4. Candidate Management Endpoints

#### Add Candidate
Add a candidate to an election.

**Endpoint:** `POST /elections/{election_id}/candidates`

**Request Body:**
```json
{
    "candidate_name": "Jane Smith",
    "party_name": "Democratic Party",
    "symbol_image": "base64_encoded_image_data"
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "candidate_id": "CAND_002",
        "election_id": "ELEC_001",
        "status": "active"
    },
    "message": "Candidate added successfully"
}
```

#### Get Candidate List
Retrieve list of candidates for an election.

**Endpoint:** `GET /elections/{election_id}/candidates`

**Response:**
```json
{
    "success": true,
    "data": {
        "candidates": [
            {
                "candidate_id": "CAND_001",
                "candidate_name": "John Smith",
                "party_name": "Progressive Party",
                "symbol_url": "https://example.com/symbols/progressive.png",
                "votes": 25000,
                "vote_percentage": 55.6
            }
        ]
    }
}
```

#### Update Candidate
Update candidate information.

**Endpoint:** `PUT /candidates/{candidate_id}`

**Request Body:**
```json
{
    "candidate_name": "John A. Smith",
    "party_name": "Progressive Party USA"
}
```

### 5. Voting Endpoints

#### Cast Vote
Cast a vote for a candidate.

**Endpoint:** `POST /votes`

**Request Body:**
```json
{
    "voter_id": "VOT123456789",
    "election_id": "ELEC_001",
    "candidate_id": "CAND_001",
    "biometric_data": {
        "face_scan": "base64_encoded_face_data",
        "fingerprint": "base64_encoded_fingerprint_data"
    }
}
```

**Response:**
```json
{
    "success": true,
    "data": {
        "vote_id": "VOTE_123456789",
        "transaction_id": "0x7f9a2b3c4d5e6f...",
        "block_hash": "a1b2c3d4e5f6...",
        "timestamp": "2024-05-15T11:00:00Z"
    },
    "message": "Vote cast successfully"
}
```

#### Verify Vote
Verify vote integrity using transaction ID.

**Endpoint:** `GET /votes/verify/{transaction_id}`

**Response:**
```json
{
    "success": true,
    "data": {
        "transaction_id": "0x7f9a2b3c4d5e6f...",
        "voter_id": "VOT123456789",
        "election_id": "ELEC_001",
        "candidate_id": "CAND_001",
        "timestamp": "2024-05-15T11:00:00Z",
        "block_hash": "a1b2c3d4e5f6...",
        "is_valid": true
    }
}
```

#### Get Voting Results
Retrieve real-time voting results.

**Endpoint:** `GET /elections/{election_id}/results`

**Query Parameters:**
- `live`: Set to 'true' for live results
- `constituency`: Filter by constituency

**Response:**
```json
{
    "success": true,
    "data": {
        "election_id": "ELEC_001",
        "total_votes": 45000,
        "voting_percentage": 45.0,
        "last_updated": "2024-05-15T11:30:00Z",
        "results": [
            {
                "candidate_id": "CAND_001",
                "candidate_name": "John Smith",
                "party_name": "Progressive Party",
                "votes": 25000,
                "vote_percentage": 55.6,
                "leading": true
            }
        ]
    }
}
```

### 6. Blockchain Endpoints

#### Get Block Information
Retrieve blockchain block information.

**Endpoint:** `GET /blockchain/blocks/{block_hash}`

**Response:**
```json
{
    "success": true,
    "data": {
        "block_hash": "a1b2c3d4e5f6...",
        "previous_block_hash": "z9y8x7w6v5u4...",
        "timestamp": "2024-05-15T11:00:00Z",
        "data": {
            "vote_id": "VOTE_123456789",
            "voter_id": "VOT123456789",
            "candidate_id": "CAND_001"
        },
        "nonce": 12345,
        "difficulty": 4
    }
}
```

#### Verify Blockchain Integrity
Verify the integrity of the entire blockchain.

**Endpoint:** `GET /blockchain/verify`

**Response:**
```json
{
    "success": true,
    "data": {
        "is_valid": true,
        "total_blocks": 45000,
        "verified_at": "2024-05-15T11:30:00Z",
        "last_block_hash": "a1b2c3d4e5f6..."
    }
}
```

### 7. Statistics Endpoints

#### Get System Statistics
Retrieve overall system statistics.

**Endpoint:** `GET /statistics/system`

**Response:**
```json
{
    "success": true,
    "data": {
        "total_elections": 15,
        "active_elections": 3,
        "total_voters": 1500000,
        "total_votes_cast": 675000,
        "average_voting_percentage": 45.0,
        "system_uptime": "99.9%",
        "last_updated": "2024-05-15T11:30:00Z"
    }
}
```

#### Get Election Statistics
Retrieve detailed statistics for a specific election.

**Endpoint:** `GET /statistics/elections/{election_id}`

**Response:**
```json
{
    "success": true,
    "data": {
        "election_id": "ELEC_001",
        "total_voters": 100000,
        "votes_cast": 45000,
        "voting_percentage": 45.0,
        "votes_by_hour": [
            {"hour": "08:00", "votes": 500},
            {"hour": "09:00", "votes": 1200}
        ],
        "votes_by_constituency": [
            {
                "constituency": "North District",
                "votes": 15000,
                "percentage": 33.3
            }
        ]
    }
}
```

## SDKs and Libraries

### Python SDK
```python
from voting_system_sdk import VotingSystemClient

# Initialize client
client = VotingSystemClient(
    api_key="YOUR_API_KEY",
    base_url="https://api.votingsystem.com/v1"
)

# Cast a vote
result = client.votes.cast(
    voter_id="VOT123456789",
    election_id="ELEC_001",
    candidate_id="CAND_001"
)

print(result.transaction_id)
```

### JavaScript SDK
```javascript
import { VotingSystemClient } from 'voting-system-sdk';

// Initialize client
const client = new VotingSystemClient({
    apiKey: 'YOUR_API_KEY',
    baseUrl: 'https://api.votingsystem.com/v1'
});

// Get election results
const results = await client.elections.getResults('ELEC_001');
console.log(results.data);
```

### cURL Examples

#### Cast Vote
```bash
curl -X POST https://api.votingsystem.com/v1/votes \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "voter_id": "VOT123456789",
    "election_id": "ELEC_001",
    "candidate_id": "CAND_001"
  }'
```

#### Get Election Results
```bash
curl -X GET https://api.votingsystem.com/v1/elections/ELEC_001/results \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Webhooks

### Configure Webhook
Receive real-time notifications about voting events.

**Endpoint:** `POST /webhooks`

**Request Body:**
```json
{
    "url": "https://your-domain.com/webhook",
    "events": ["vote_cast", "election_completed", "candidate_added"],
    "secret": "your_webhook_secret"
}
```

### Webhook Payload Example
```json
{
    "event": "vote_cast",
    "data": {
        "vote_id": "VOTE_123456789",
        "election_id": "ELEC_001",
        "candidate_id": "CAND_001",
        "timestamp": "2024-05-15T11:00:00Z"
    },
    "signature": "sha256=5d41402abc4b2a76b9719d911017c592"
}
```

## Testing

### Sandbox Environment
Test your integration in a safe sandbox environment.

**Sandbox URL:** `https://sandbox-api.votingsystem.com/v1`

### Test Data
Use test credentials for development:
```
API Key: test_api_key_12345
Test Voter ID: TEST_VOTER_001
Test Election ID: TEST_ELEC_001
Test Candidate ID: TEST_CAND_001
```

## Rate Limits and Quotas

### Standard Plan
- 100 requests per minute
- 10,000 requests per day
- Email support

### Premium Plan
- 1,000 requests per minute
- 100,000 requests per day
- Priority support
- Webhook support

### Enterprise Plan
- Unlimited requests
- Custom rate limits
- Dedicated support
- SLA guarantee

## Support

### Technical Support
- Email: api-support@votingsystem.com
- Documentation: https://docs.votingsystem.com
- Status Page: https://status.votingsystem.com

### Community
- GitHub: https://github.com/votingsystem/api
- Stack Overflow: #voting-system-api
- Discord: https://discord.gg/votingsystem

---

**Note**: This API documentation is for development purposes. Production usage requires proper authentication and compliance with election regulations.
