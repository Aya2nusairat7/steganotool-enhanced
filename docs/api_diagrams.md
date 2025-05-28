 # API Architecture Diagrams

This document provides detailed UML diagrams for the API layer of the steganography system.

## 1. API Endpoint Overview

```mermaid
graph TB
    subgraph "Authentication Endpoints"
        SignIn[POST /api/auth/sign-in]
        SignUp[POST /api/auth/sign-up]
    end
    
    subgraph "Core Steganography Endpoints"
        Encrypt[POST /api/encrypt]
        Decrypt[POST /api/decrypt]
        Download[GET /api/download/:filename]
    end
    
    subgraph "QR Code Endpoints"
        GenerateQR[POST /api/generate-qr]
        EncryptQR[POST /api/encrypt-qr]
        DecryptQR[POST /api/decrypt-qr]
    end
    
    subgraph "Utility Endpoints"
        Health[GET /api/health]
        Capabilities[GET /api/capabilities]
    end
    
    subgraph "Web Interface"
        Index[GET /]
        SignInPage[GET /sign-in]
        SignUpPage[GET /sign-up]
    end
    
    %% Authentication flow
    SignIn --> Encrypt
    SignIn --> Decrypt
    SignIn --> GenerateQR
    SignIn --> EncryptQR
    SignIn --> DecryptQR
    SignIn --> Download
    
    %% Processing flow
    Encrypt --> Download
    EncryptQR --> Download
    
    %% Styling
    classDef auth fill:#ffebee
    classDef core fill:#e8f5e8
    classDef qr fill:#e3f2fd
    classDef utility fill:#fff3e0
    classDef web fill:#f3e5f5
    
    class SignIn,SignUp auth
    class Encrypt,Decrypt,Download core
    class GenerateQR,EncryptQR,DecryptQR qr
    class Health,Capabilities utility
    class Index,SignInPage,SignUpPage web
```

## 2. Request/Response Flow Diagram

```mermaid
sequenceDiagram
    participant Client
    participant AuthMiddleware
    participant APIRoute
    participant Service
    participant FileSystem
    participant Response
    
    Client->>+AuthMiddleware: HTTP Request + Headers
    
    alt Authentication Required
        AuthMiddleware->>AuthMiddleware: Check Authorization Header
        AuthMiddleware->>AuthMiddleware: Validate Token/Session
        
        alt Invalid Auth
            AuthMiddleware-->>Client: 401 Unauthorized
        end
    end
    
    AuthMiddleware->>+APIRoute: Authorized Request
    
    APIRoute->>APIRoute: Validate Request Data
    APIRoute->>APIRoute: Parse Form/JSON Data
    
    alt Invalid Request
        APIRoute-->>Client: 400 Bad Request
    end
    
    APIRoute->>+Service: Process Business Logic
    Service->>Service: Execute Core Operations
    
    alt File Operations Required
        Service->>+FileSystem: Read/Write Files
        FileSystem-->>-Service: File Operations Result
    end
    
    Service-->>-APIRoute: Processing Result
    
    APIRoute->>+Response: Format Response
    Response->>Response: Add Headers
    Response->>Response: Set Status Code
    Response-->>-APIRoute: Formatted Response
    
    APIRoute-->>-AuthMiddleware: Response Data
    AuthMiddleware-->>-Client: HTTP Response
```

## 3. Authentication Flow Diagram

```mermaid
sequenceDiagram
    participant Client
    participant SignInEndpoint
    participant AuthService
    participant Session
    
    Note over Client,Session: Sign-In Process
    
    Client->>+SignInEndpoint: POST /api/auth/sign-in
    Note right of Client: {email, password}
    
    SignInEndpoint->>SignInEndpoint: Validate Input
    
    alt Missing Credentials
        SignInEndpoint-->>Client: 400 Bad Request
    end
    
    SignInEndpoint->>+AuthService: Authenticate User
    AuthService->>AuthService: Verify Credentials
    
    alt Invalid Credentials
        AuthService-->>SignInEndpoint: Authentication Failed
        SignInEndpoint-->>Client: 401 Unauthorized
    end
    
    AuthService->>AuthService: Generate Token
    AuthService-->>-SignInEndpoint: Token + User Info
    
    SignInEndpoint->>+Session: Store Session Data
    Session-->>-SignInEndpoint: Session Created
    
    SignInEndpoint-->>-Client: 200 OK + Token
    Note right of Client: {status, token, user}
    
    Note over Client,Session: Subsequent API Calls
    
    Client->>+SignInEndpoint: API Request + Authorization Header
    SignInEndpoint->>SignInEndpoint: Validate Token
    SignInEndpoint-->>-Client: Authorized Response
```

## 4. File Upload and Processing Flow

```mermaid
flowchart TD
    Start([Client Upload Request]) --> ValidateAuth{Authentication Valid?}
    ValidateAuth -->|No| AuthError[Return 401 Unauthorized]
    ValidateAuth -->|Yes| CheckFile{File Present?}
    
    CheckFile -->|No| FileError[Return 400 Bad Request]
    CheckFile -->|Yes| ValidateFile[Validate File Type]
    
    ValidateFile --> CheckSize{File Size OK?}
    CheckSize -->|No| SizeError[Return 413 Payload Too Large]
    CheckSize -->|Yes| SecureFilename[Generate Secure Filename]
    
    SecureFilename --> SaveTemp[Save to Temporary Location]
    SaveTemp --> ProcessFile[Process File Based on Type]
    
    ProcessFile --> ImageProcess{Image File?}
    ProcessFile --> AudioProcess{Audio File?}
    
    ImageProcess -->|Yes| ConvertImage[Convert to PNG if needed]
    AudioProcess -->|Yes| ConvertAudio[Convert to WAV if needed]
    
    ConvertImage --> EmbedData[Embed Data using LSB]
    ConvertAudio --> EmbedData
    
    EmbedData --> SaveOutput[Save to Output Directory]
    SaveOutput --> GenerateResponse[Generate Success Response]
    GenerateResponse --> Cleanup[Cleanup Temporary Files]
    Cleanup --> End([Return Response to Client])
    
    AuthError --> End
    FileError --> End
    SizeError --> End
```

## 5. Error Handling Flow

```mermaid
stateDiagram-v2
    [*] --> RequestReceived : HTTP Request
    
    RequestReceived --> AuthCheck : Check Authentication
    AuthCheck --> AuthFailed : Invalid Token
    AuthCheck --> InputValidation : Valid Token
    
    AuthFailed --> ErrorResponse : 401 Unauthorized
    
    InputValidation --> ValidationFailed : Invalid Input
    InputValidation --> FileProcessing : Valid Input
    
    ValidationFailed --> ErrorResponse : 400 Bad Request
    
    FileProcessing --> ProcessingFailed : Processing Error
    FileProcessing --> Success : Processing Complete
    
    ProcessingFailed --> ErrorResponse : 500 Internal Server Error
    
    Success --> SuccessResponse : 200 OK
    
    ErrorResponse --> LogError : Log Error Details
    SuccessResponse --> LogSuccess : Log Success
    
    LogError --> [*] : Return Error Response
    LogSuccess --> [*] : Return Success Response
```

## 6. API Response Structure Diagram

```mermaid
classDiagram
    class APIResponse {
        <<interface>>
        +status: string
        +timestamp: datetime
        +request_id: string
    }
    
    class SuccessResponse {
        +status: "success"
        +data: object
        +message?: string
    }
    
    class ErrorResponse {
        +status: "error"
        +error: string
        +code: number
        +details?: object
    }
    
    class EncryptResponse {
        +original_filename: string
        +output_filename: string
        +file_size: number
        +message_length: number
        +compression_ratio: number
        +download_url: string
        +encryption_method: string
    }
    
    class DecryptResponse {
        +filename: string
        +message: string
        +message_length: number
        +password_found: boolean
        +encryption_method: string
    }
    
    class HealthResponse {
        +status: "healthy"
        +version?: string
        +uptime?: number
    }
    
    class CapabilitiesResponse {
        +image_steganography: boolean
        +audio_steganography: boolean
        +qr_code_support: boolean
        +supported_formats: array
    }
    
    APIResponse <|-- SuccessResponse
    APIResponse <|-- ErrorResponse
    SuccessResponse <|-- EncryptResponse
    SuccessResponse <|-- DecryptResponse
    SuccessResponse <|-- HealthResponse
    SuccessResponse <|-- CapabilitiesResponse
```

## 7. Middleware Chain Diagram

```mermaid
flowchart LR
    Request[HTTP Request] --> CORS[CORS Middleware]
    CORS --> Auth[Authentication Middleware]
    Auth --> RateLimit[Rate Limiting]
    RateLimit --> Validation[Request Validation]
    Validation --> Route[Route Handler]
    Route --> Business[Business Logic]
    Business --> Response[Response Formatter]
    Response --> Logger[Access Logger]
    Logger --> Output[HTTP Response]
    
    %% Error paths
    CORS -.->|CORS Error| ErrorHandler[Error Handler]
    Auth -.->|Auth Error| ErrorHandler
    RateLimit -.->|Rate Limit| ErrorHandler
    Validation -.->|Validation Error| ErrorHandler
    Route -.->|Route Error| ErrorHandler
    Business -.->|Business Error| ErrorHandler
    
    ErrorHandler --> Logger
    
    %% Styling
    classDef middleware fill:#e3f2fd
    classDef handler fill:#e8f5e8
    classDef error fill:#ffebee
    
    class CORS,Auth,RateLimit,Validation middleware
    class Route,Business,Response,Logger handler
    class ErrorHandler error
```

## 8. API Security Model

```mermaid
graph TB
    subgraph "Client Layer"
        WebClient[Web Client]
        APIClient[API Client]
    end
    
    subgraph "Security Layer"
        HTTPS[HTTPS/TLS]
        Auth[Authentication]
        CSRF[CSRF Protection]
        RateLimit[Rate Limiting]
        InputVal[Input Validation]
    end
    
    subgraph "Application Layer"
        Routes[API Routes]
        Business[Business Logic]
    end
    
    subgraph "Data Layer"
        FileSystem[File System]
        TempStorage[Temporary Storage]
    end
    
    %% Security flow
    WebClient --> HTTPS
    APIClient --> HTTPS
    HTTPS --> Auth
    Auth --> CSRF
    CSRF --> RateLimit
    RateLimit --> InputVal
    InputVal --> Routes
    
    %% Application flow
    Routes --> Business
    Business --> FileSystem
    Business --> TempStorage
    
    %% Security measures
    Auth -.->|Token Validation| Routes
    InputVal -.->|Sanitization| Business
    RateLimit -.->|Throttling| Routes
    
    %% Styling
    classDef client fill:#e3f2fd
    classDef security fill:#ffebee
    classDef app fill:#e8f5e8
    classDef data fill:#fff3e0
    
    class WebClient,APIClient client
    class HTTPS,Auth,CSRF,RateLimit,InputVal security
    class Routes,Business app
    class FileSystem,TempStorage data
```

## API Endpoint Details

### Core Endpoints

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/api/health` | GET | Health check | No |
| `/api/capabilities` | GET | Get system capabilities | No |
| `/api/encrypt` | POST | Encrypt and hide message | Yes |
| `/api/decrypt` | POST | Extract and decrypt message | Yes |
| `/api/download/:filename` | GET | Download processed file | Yes |

### QR Code Endpoints

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/api/generate-qr` | POST | Generate QR code | Yes |
| `/api/encrypt-qr` | POST | Create encrypted QR code | Yes |
| `/api/decrypt-qr` | POST | Decrypt QR code message | Yes |

### Authentication Endpoints

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|----------------|
| `/api/auth/sign-in` | POST | User authentication | No |
| `/api/auth/sign-up` | POST | User registration | No |

### Response Codes

- **200 OK**: Successful operation
- **400 Bad Request**: Invalid input or missing parameters
- **401 Unauthorized**: Authentication required or invalid
- **413 Payload Too Large**: File size exceeds limit
- **500 Internal Server Error**: Server processing error