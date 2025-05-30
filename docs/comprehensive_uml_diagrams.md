# Comprehensive UML Diagrams - Steganography System

This document contains all major UML diagram types for the steganography system using proper Mermaid.js syntax.

## 1. Use Case Diagrams

### Primary Use Cases

```mermaid
graph TB
    subgraph "Steganography System"
        UC1[Encrypt Message in Image]
        UC2[Decrypt Message from Image]
        UC3[Encrypt Message in Audio]
        UC4[Decrypt Message from Audio]
        UC5[Generate QR Code]
        UC6[Encrypt Message in QR Code]
        UC7[Decrypt Message from QR Code]
        UC8[Auto-Generate Password]
        UC9[Manage File Uploads]
        UC10[Download Processed Files]
        UC11[User Authentication]
        UC12[View System Capabilities]
    end
    
    subgraph "Actors"
        User[👤 End User]
        Developer[👨‍💻 Developer]
        Admin[👨‍💼 Administrator]
        APIClient[🤖 API Client]
    end
    
    %% User interactions
    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
    User --> UC6
    User --> UC7
    User --> UC8
    User --> UC9
    User --> UC10
    User --> UC11
    
    %% Developer interactions
    Developer --> UC12
    Developer --> UC1
    Developer --> UC2
    
    %% API Client interactions
    APIClient --> UC1
    APIClient --> UC2
    APIClient --> UC6
    APIClient --> UC7
    APIClient --> UC12
    
    %% Admin interactions
    Admin --> UC11
    Admin --> UC12
    
    %% Include relationships
    UC1 -.->|includes| UC8
    UC3 -.->|includes| UC8
    UC6 -.->|includes| UC8
    UC1 -.->|includes| UC9
    UC3 -.->|includes| UC9
    UC6 -.->|includes| UC9
    UC1 -.->|includes| UC10
    UC3 -.->|includes| UC10
    UC6 -.->|includes| UC10
    
    %% Extend relationships
    UC2 -.->|extends| UC11
    UC4 -.->|extends| UC11
    UC7 -.->|extends| UC11
```

### Authentication Use Cases

```mermaid
graph TB
    subgraph "Authentication System"
        UC_AUTH1[Sign In]
        UC_AUTH2[Sign Up]
        UC_AUTH3[Generate Auth Token]
        UC_AUTH4[Validate Token]
        UC_AUTH5[Logout]
        UC_AUTH6[Session Management]
    end
    
    subgraph "Actors"
        NewUser[👤 New User]
        ExistingUser[👤 Existing User]
        System[🖥️ System]
    end
    
    NewUser --> UC_AUTH2
    ExistingUser --> UC_AUTH1
    ExistingUser --> UC_AUTH5
    
    UC_AUTH1 -.->|includes| UC_AUTH3
    UC_AUTH2 -.->|includes| UC_AUTH3
    UC_AUTH3 -.->|includes| UC_AUTH6
    
    System --> UC_AUTH4
    System --> UC_AUTH6
```

## 2. Object Diagrams

### Encryption Process Objects

```mermaid
graph TB
    subgraph "Encryption Process Instance"
        msg1[message1: Message<br/>content: "Secret text"<br/>size: 256 bytes<br/>encoding: "UTF-8"]
        
        comp1[compression1: CompressionInfo<br/>original_size: 256<br/>compressed_size: 180<br/>ratio: 29.7%<br/>would_compress: true]
        
        enc1[encrypted1: EncryptedData<br/>salt: [16 bytes]<br/>iv: [16 bytes]<br/>ciphertext: [180 bytes]<br/>total_size: 212 bytes]
        
        file1[image1: MediaFile<br/>filename: "photo.jpg"<br/>format: "JPEG"<br/>size: 2048000<br/>capacity: 768000]
        
        stego1[stego1: SteganographicFile<br/>output_path: "stego_photo.png"<br/>hidden_data_size: 212<br/>password_embedded: true]
        
        result1[result1: ProcessingResult<br/>status: "success"<br/>compression_ratio: 29.7%<br/>file_size: 2048500<br/>download_url: "/api/download/stego_photo.png"]
    end
    
    msg1 --> comp1
    comp1 --> enc1
    file1 --> stego1
    enc1 --> stego1
    stego1 --> result1
```

### QR Code Process Objects

```mermaid
graph TB
    subgraph "QR Code Generation Instance"
        qr_msg[qrMessage: Message<br/>content: "Hidden data"<br/>size: 128 bytes]
        
        qr_enc[qrEncrypted: EncryptedData<br/>salt: [16 bytes]<br/>iv: [16 bytes]<br/>ciphertext: [128 bytes]<br/>marker: 0x01<br/>password: "auto123"]
        
        qr_code[qrCode: QRCode<br/>data: [encrypted payload]<br/>error_correction: "H"<br/>size: 512x512<br/>style: "fancy"]
        
        qr_result[qrResult: ProcessingResult<br/>status: "success"<br/>output_filename: "qr_encrypted_abc123.png"<br/>auto_generated_password: "auto123"]
    end
    
    qr_msg --> qr_enc
    qr_enc --> qr_code
    qr_code --> qr_result
```

## 3. Package and Class Diagrams

### Package Diagram

```mermaid
graph TB
    subgraph "Steganography System Packages"
        subgraph "Web Layer"
            WebPkg[📦 web<br/>- templates/<br/>- static/<br/>- Flask routes]
        end
        
        subgraph "API Layer"
            APIPkg[📦 api<br/>- REST endpoints<br/>- Authentication<br/>- Request handling]
        end
        
        subgraph "Core Services"
            CorePkg[📦 core<br/>- Encryption<br/>- Compression<br/>- Steganography]
        end
        
        subgraph "Media Processing"
            MediaPkg[📦 media<br/>- Image processing<br/>- Audio processing<br/>- Format conversion]
        end
        
        subgraph "QR Code Services"
            QRPkg[📦 qr<br/>- QR generation<br/>- QR steganography<br/>- Style processing]
        end
        
        subgraph "Utilities"
            UtilsPkg[📦 utils<br/>- File management<br/>- Security<br/>- Helpers]
        end
        
        subgraph "Client"
            ClientPkg[📦 client<br/>- CLI interface<br/>- API client<br/>- Command handlers]
        end
        
        subgraph "Testing"
            TestPkg[📦 tests<br/>- Unit tests<br/>- Integration tests<br/>- Test utilities]
        end
    end
    
    WebPkg --> APIPkg
    APIPkg --> CorePkg
    APIPkg --> MediaPkg
    APIPkg --> QRPkg
    CorePkg --> UtilsPkg
    MediaPkg --> UtilsPkg
    QRPkg --> CorePkg
    ClientPkg --> APIPkg
    TestPkg --> CorePkg
    TestPkg --> APIPkg
```

### Detailed Class Diagram

```mermaid
classDiagram
    class FlaskApplication {
        +config: dict
        +secret_key: string
        +upload_folder: string
        +output_folder: string
        +run(host, port, debug)
        +create_directories()
        +register_routes()
    }
    
    class APIController {
        +encrypt_endpoint()
        +decrypt_endpoint()
        +qr_encrypt_endpoint()
        +qr_decrypt_endpoint()
        +download_endpoint()
        +health_check()
        +capabilities()
    }
    
    class AuthenticationService {
        +sign_in(email, password)
        +sign_up(user_data)
        +generate_token(user)
        +validate_token(token)
        +require_auth(func)
    }
    
    class EncryptionEngine {
        -PBKDF2_ITERATIONS: int
        -AES_KEY_SIZE: int
        +encrypt_message(message, password)
        +decrypt_message(data, password)
        +derive_key(password, salt)
        +generate_salt()
        +generate_iv()
    }
    
    class CompressionEngine {
        +compress_data(data)
        +decompress_data(data)
        +get_compression_info(message)
        +calculate_ratio(original, compressed)
        -is_compression_beneficial(original, compressed)
    }
    
    class SteganographyEngine {
        +hide_data_in_image(input_path, output_path, data)
        +extract_data_from_image(image_path)
        +hide_data_in_audio(input_path, output_path, data)
        +extract_data_from_audio(audio_path)
        +calculate_capacity(media_file)
    }
    
    class QRCodeEngine {
        +generate_qr_code(data, output_path, options)
        +hide_message_in_qr(message, password, output_path)
        +extract_message_from_qr(qr_path, password)
        +apply_style(qr_code, style, background)
    }
    
    class MediaProcessor {
        +convert_audio_to_wav(input_path)
        +convert_and_hide_in_image(input_path, output_path, data)
        +validate_image_format(file_path)
        +validate_audio_format(file_path)
        +get_media_info(file_path)
    }
    
    class FileManager {
        +secure_filename(filename)
        +save_uploaded_file(file, path)
        +cleanup_temp_files()
        +get_file_size(path)
        +validate_file_size(file)
    }
    
    class CLIClient {
        +main()
        +encrypt_command(args)
        +decrypt_command(args)
        +qr_encrypt_command(args)
        +qr_decrypt_command(args)
        +health_check_command(args)
    }
    
    %% Relationships
    FlaskApplication --> APIController
    APIController --> AuthenticationService
    APIController --> EncryptionEngine
    APIController --> CompressionEngine
    APIController --> SteganographyEngine
    APIController --> QRCodeEngine
    APIController --> MediaProcessor
    APIController --> FileManager
    
    EncryptionEngine --> CompressionEngine
    SteganographyEngine --> MediaProcessor
    QRCodeEngine --> EncryptionEngine
    QRCodeEngine --> CompressionEngine
    
    CLIClient --> APIController
    
    %% Inheritance
    EncryptionEngine <|-- QRCodeEngine : uses
    MediaProcessor <|-- SteganographyEngine : uses
```

## 4. Component Diagram

```mermaid
graph TB
    subgraph "Client Tier"
        WebUI[🌐 Web Interface<br/>HTML/CSS/JavaScript]
        CLI[💻 CLI Client<br/>Python Command Line]
        APIClient[🔌 API Client<br/>HTTP Requests]
    end
    
    subgraph "Application Tier"
        subgraph "Web Server"
            Flask[🌶️ Flask Application<br/>WSGI Server]
            Routes[🛣️ API Routes<br/>REST Endpoints]
            Auth[🔐 Authentication<br/>Token Validation]
        end
        
        subgraph "Core Services"
            EncryptSvc[🔒 Encryption Service<br/>AES-256-CBC]
            CompressSvc[📦 Compression Service<br/>zlib Algorithm]
            StegoSvc[🖼️ Steganography Service<br/>LSB Embedding]
            QRSvc[📱 QR Code Service<br/>Generation & Processing]
        end
        
        subgraph "Media Processing"
            ImageProc[🖼️ Image Processor<br/>PIL/Pillow]
            AudioProc[🎵 Audio Processor<br/>Wave Processing]
            Converter[🔄 Format Converter<br/>FFmpeg Integration]
        end
        
        subgraph "Utilities"
            FileManager[📁 File Manager<br/>Upload/Download]
            Security[🛡️ Security Utils<br/>Validation/Sanitization]
            Logger[📝 Logger<br/>Event Tracking]
        end
    end
    
    subgraph "Data Tier"
        TempStorage[💾 Temporary Storage<br/>uploads/ directory]
        OutputStorage[📤 Output Storage<br/>output/ directory]
        StaticFiles[📄 Static Files<br/>CSS/JS/Images]
    end
    
    %% Client connections
    WebUI --> Flask
    CLI --> Routes
    APIClient --> Routes
    
    %% Internal connections
    Flask --> Routes
    Routes --> Auth
    Routes --> EncryptSvc
    Routes --> CompressSvc
    Routes --> StegoSvc
    Routes --> QRSvc
    Routes --> FileManager
    
    %% Service dependencies
    EncryptSvc --> CompressSvc
    StegoSvc --> ImageProc
    StegoSvc --> AudioProc
    QRSvc --> EncryptSvc
    ImageProc --> Converter
    AudioProc --> Converter
    
    %% Utility connections
    FileManager --> Security
    Routes --> Logger
    FileManager --> TempStorage
    FileManager --> OutputStorage
    Flask --> StaticFiles
    
    %% Styling
    classDef client fill:#e1f5fe
    classDef app fill:#f3e5f5
    classDef data fill:#e8f5e8
    
    class WebUI,CLI,APIClient client
    class Flask,Routes,Auth,EncryptSvc,CompressSvc,StegoSvc,QRSvc,ImageProc,AudioProc,Converter,FileManager,Security,Logger app
    class TempStorage,OutputStorage,StaticFiles data
```

## 5. Deployment Diagram

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Load Balancer Tier"
            LB[⚖️ Load Balancer<br/>Nginx/HAProxy<br/>Port 80/443]
        end
        
        subgraph "Application Tier"
            subgraph "Web Server 1"
                App1[🌶️ Flask App Instance 1<br/>Python 3.8+<br/>Port 8080]
                Worker1[👷 Gunicorn Workers<br/>4 processes]
            end
            
            subgraph "Web Server 2"
                App2[🌶️ Flask App Instance 2<br/>Python 3.8+<br/>Port 8081]
                Worker2[👷 Gunicorn Workers<br/>4 processes]
            end
        end
        
        subgraph "File Storage Tier"
            SharedFS[📁 Shared File System<br/>NFS/GlusterFS<br/>uploads/ & output/]
        end
        
        subgraph "Monitoring Tier"
            Monitor[📊 Monitoring<br/>Prometheus/Grafana]
            Logs[📝 Log Aggregation<br/>ELK Stack]
        end
    end
    
    subgraph "Development Environment"
        DevServer[💻 Development Server<br/>Flask Dev Server<br/>localhost:8080]
        LocalFS[📁 Local File System<br/>uploads/ & output/]
    end
    
    subgraph "Client Environment"
        Browser[🌐 Web Browser<br/>Chrome/Firefox/Safari]
        CLITool[💻 CLI Tool<br/>Python Client]
        Mobile[📱 Mobile Browser<br/>Responsive UI]
    end
    
    subgraph "External Dependencies"
        FFmpeg[🎬 FFmpeg<br/>Audio Conversion<br/>System Package]
        Python[🐍 Python Runtime<br/>3.8+ with pip<br/>Virtual Environment]
    end
    
    %% Production connections
    Browser --> LB
    Mobile --> LB
    CLITool --> LB
    
    LB --> App1
    LB --> App2
    
    App1 --> Worker1
    App2 --> Worker2
    
    App1 --> SharedFS
    App2 --> SharedFS
    
    App1 --> Monitor
    App2 --> Monitor
    App1 --> Logs
    App2 --> Logs
    
    %% Development connections
    Browser -.-> DevServer
    CLITool -.-> DevServer
    DevServer -.-> LocalFS
    
    %% Dependencies
    App1 --> FFmpeg
    App2 --> FFmpeg
    App1 --> Python
    App2 --> Python
    DevServer --> FFmpeg
    DevServer --> Python
    
    %% Styling
    classDef prod fill:#ffebee
    classDef dev fill:#e8f5e8
    classDef client fill:#e3f2fd
    classDef external fill:#fff3e0
    
    class LB,App1,App2,Worker1,Worker2,SharedFS,Monitor,Logs prod
    class DevServer,LocalFS dev
    class Browser,CLITool,Mobile client
    class FFmpeg,Python external
```

## 6. Activity Diagram

### Message Encryption Activity

```mermaid
flowchart TD
    Start([Start Encryption]) --> ValidateInput{Validate Input}
    ValidateInput -->|Invalid| ErrorInput[Return Input Error]
    ValidateInput -->|Valid| CheckAuth{Check Authentication}
    
    CheckAuth -->|Unauthorized| ErrorAuth[Return Auth Error]
    CheckAuth -->|Authorized| SaveFile[Save Uploaded File]
    
    SaveFile --> GetMessage[Extract Message]
    GetMessage --> CheckCompression{Check if Compression Beneficial}
    
    CheckCompression -->|Yes| CompressData[Compress Message with zlib]
    CheckCompression -->|No| SkipCompression[Skip Compression]
    
    CompressData --> CheckPassword{Password Provided?}
    SkipCompression --> CheckPassword
    
    CheckPassword -->|No| GeneratePassword[Auto-Generate Secure Password]
    CheckPassword -->|Yes| UsePassword[Use Provided Password]
    
    GeneratePassword --> EncryptData[Encrypt Data with AES-256]
    UsePassword --> EncryptData
    
    EncryptData --> EmbedPassword{Embed Password?}
    EmbedPassword -->|Yes| AddPasswordMarker[Add Password Marker + Password]
    EmbedPassword -->|No| SkipPasswordEmbed[Skip Password Embedding]
    
    AddPasswordMarker --> CheckMediaType{Media Type?}
    SkipPasswordEmbed --> CheckMediaType
    
    CheckMediaType -->|Image| ProcessImage[Hide Data in Image using LSB]
    CheckMediaType -->|Audio| ProcessAudio[Hide Data in Audio Samples]
    CheckMediaType -->|QR Code| ProcessQR[Generate QR Code with Data]
    
    ProcessImage --> SaveOutput[Save Steganographic File]
    ProcessAudio --> SaveOutput
    ProcessQR --> SaveOutput
    
    SaveOutput --> CalculateStats[Calculate Compression Stats]
    CalculateStats --> CreateResponse[Create Success Response]
    CreateResponse --> CleanupTemp[Cleanup Temporary Files]
    CleanupTemp --> End([End Success])
    
    ErrorInput --> End
    ErrorAuth --> End
    
    %% Error handling
    SaveFile -->|Error| ErrorFile[File Save Error]
    EncryptData -->|Error| ErrorEncrypt[Encryption Error]
    ProcessImage -->|Error| ErrorProcess[Processing Error]
    ProcessAudio -->|Error| ErrorProcess
    ProcessQR -->|Error| ErrorProcess
    
    ErrorFile --> End
    ErrorEncrypt --> End
    ErrorProcess --> End
```

### Message Decryption Activity

```mermaid
flowchart TD
    StartDecrypt([Start Decryption]) --> ValidateFile{Validate File}
    ValidateFile -->|Invalid| ErrorFileInvalid[Return File Error]
    ValidateFile -->|Valid| CheckAuthDecrypt{Check Authentication}
    
    CheckAuthDecrypt -->|Unauthorized| ErrorAuthDecrypt[Return Auth Error]
    CheckAuthDecrypt -->|Authorized| SaveUpload[Save Uploaded File]
    
    SaveUpload --> DetectMediaType{Detect Media Type}
    
    DetectMediaType -->|Image| ExtractFromImage[Extract Data from Image LSB]
    DetectMediaType -->|Audio| ExtractFromAudio[Extract Data from Audio]
    DetectMediaType -->|QR Code| ExtractFromQR[Extract Data from QR Code]
    
    ExtractFromImage --> CheckDataExists{Data Found?}
    ExtractFromAudio --> CheckDataExists
    ExtractFromQR --> CheckDataExists
    
    CheckDataExists -->|No| ErrorNoData[No Hidden Data Found]
    CheckDataExists -->|Yes| SearchPassword[Search for Embedded Password]
    
    SearchPassword --> CheckPasswordFound{Password Found?}
    CheckPasswordFound -->|Yes| UseEmbeddedPassword[Use Embedded Password]
    CheckPasswordFound -->|No| CheckProvidedPassword{Password Provided?}
    
    CheckProvidedPassword -->|No| ErrorNoPassword[No Password Available]
    CheckProvidedPassword -->|Yes| UseProvidedPassword[Use Provided Password]
    
    UseEmbeddedPassword --> AttemptDecryption[Attempt Decryption]
    UseProvidedPassword --> AttemptDecryption
    
    AttemptDecryption --> TryXOR[Try XOR Decryption First]
    TryXOR --> CheckXORValid{Valid UTF-8?}
    
    CheckXORValid -->|Yes| CheckCompressed{Check if Compressed}
    CheckXORValid -->|No| TryAES[Try AES Decryption]
    
    TryAES --> CheckAESValid{AES Successful?}
    CheckAESValid -->|No| ErrorDecryption[Decryption Failed]
    CheckAESValid -->|Yes| CheckCompressed
    
    CheckCompressed -->|Yes| DecompressData[Decompress with zlib]
    CheckCompressed -->|No| SkipDecompression[Skip Decompression]
    
    DecompressData --> ValidateMessage{Valid Message?}
    SkipDecompression --> ValidateMessage
    
    ValidateMessage -->|Invalid| ErrorInvalidMessage[Invalid Message Format]
    ValidateMessage -->|Valid| CreateDecryptResponse[Create Success Response]
    
    CreateDecryptResponse --> CleanupTempDecrypt[Cleanup Temporary Files]
    CleanupTempDecrypt --> EndDecrypt([End Success])
    
    %% Error paths
    ErrorFileInvalid --> EndDecrypt
    ErrorAuthDecrypt --> EndDecrypt
    ErrorNoData --> EndDecrypt
    ErrorNoPassword --> EndDecrypt
    ErrorDecryption --> EndDecrypt
    ErrorInvalidMessage --> EndDecrypt
```

## 7. Sequence Diagram

### Complete Encryption Sequence

```mermaid
sequenceDiagram
    participant User
    participant WebUI
    participant APIController
    participant AuthService
    participant FileManager
    participant CompressionService
    participant EncryptionService
    participant SteganographyService
    participant MediaProcessor
    
    User->>WebUI: Upload file + message + password
    WebUI->>APIController: POST /api/encrypt
    
    APIController->>AuthService: validate_token(auth_header)
    AuthService-->>APIController: token_valid: true
    
    APIController->>FileManager: save_uploaded_file(file)
    FileManager-->>APIController: file_path: "uploads/image.jpg"
    
    APIController->>CompressionService: get_compression_info(message)
    CompressionService-->>APIController: compression_info: {ratio: 35%, beneficial: true}
    
    APIController->>CompressionService: compress_data(message)
    CompressionService-->>APIController: compressed_data: bytes
    
    APIController->>EncryptionService: encrypt_message(compressed_data, password)
    EncryptionService-->>APIController: encrypted_data: bytes
    
    APIController->>MediaProcessor: validate_image_format(file_path)
    MediaProcessor-->>APIController: format_valid: true
    
    APIController->>SteganographyService: hide_data_in_image(file_path, output_path, encrypted_data)
    SteganographyService->>MediaProcessor: convert_and_hide_in_image(file_path, output_path, data)
    MediaProcessor-->>SteganographyService: conversion_complete
    SteganographyService-->>APIController: steganography_complete
    
    APIController->>FileManager: get_file_size(output_path)
    FileManager-->>APIController: file_size: 2048576
    
    APIController->>FileManager: cleanup_temp_files()
    FileManager-->>APIController: cleanup_complete
    
    APIController-->>WebUI: success_response: {status, download_url, stats}
    WebUI-->>User: Display success + download link
```

### Authentication Sequence

```mermaid
sequenceDiagram
    participant User
    participant WebUI
    participant APIController
    participant AuthService
    participant TokenGenerator
    
    User->>WebUI: Enter credentials (email, password)
    WebUI->>APIController: POST /api/auth/sign-in
    
    APIController->>AuthService: validate_credentials(email, password)
    
    alt Valid Credentials
        AuthService->>TokenGenerator: generate_token(user_data)
        TokenGenerator-->>AuthService: auth_token: "jwt_token_string"
        AuthService-->>APIController: auth_success: {token, user_info}
        APIController-->>WebUI: success_response: {token, user}
        WebUI->>WebUI: store_token_locally(token)
        WebUI-->>User: Redirect to main interface
    else Invalid Credentials
        AuthService-->>APIController: auth_failure: "Invalid credentials"
        APIController-->>WebUI: error_response: {error: "Invalid email or password"}
        WebUI-->>User: Display error message
    end
    
    Note over WebUI: For subsequent API calls
    WebUI->>APIController: API Request + Authorization: Bearer token
    APIController->>AuthService: validate_token(token)
    AuthService-->>APIController: token_validation_result
```

### QR Code Generation Sequence

```mermaid
sequenceDiagram
    participant User
    participant WebUI
    participant APIController
    participant QRCodeService
    participant EncryptionService
    participant CompressionService
    participant FileManager
    
    User->>WebUI: Enter message + select QR style
    WebUI->>APIController: POST /api/encrypt-qr
    
    APIController->>CompressionService: get_compression_info(message)
    CompressionService-->>APIController: compression_info
    
    alt Auto-generate password
        APIController->>EncryptionService: generate_strong_password(16)
        EncryptionService-->>APIController: auto_password: "random_secure_pass"
    else Use provided password
        Note over APIController: Use user-provided password
    end
    
    APIController->>QRCodeService: hide_message_in_qr(message, password, output_path, style)
    
    QRCodeService->>CompressionService: compress_data(message)
    CompressionService-->>QRCodeService: compressed_data
    
    QRCodeService->>EncryptionService: encrypt_message(compressed_data, password)
    EncryptionService-->>QRCodeService: encrypted_data
    
    QRCodeService->>QRCodeService: generate_qr_code(encrypted_data + password_marker + password)
    QRCodeService->>QRCodeService: apply_style(qr_code, style, background_image)
    QRCodeService-->>APIController: qr_generation_complete
    
    APIController->>FileManager: get_file_size(output_path)
    FileManager-->>APIController: file_size
    
    APIController-->>WebUI: success_response: {output_filename, download_url, auto_password}
    WebUI-->>User: Display QR code + download link + password (if auto-generated)
```

## 8. State Transition Diagram

### File Processing State Machine

```mermaid
stateDiagram-v2
    [*] --> Idle
    
    Idle --> Uploading : file_upload_started
    Uploading --> ValidationPending : file_uploaded
    Uploading --> UploadError : upload_failed
    
    ValidationPending --> Validating : start_validation
    Validating --> ValidationError : validation_failed
    Validating --> Validated : validation_passed
    
    Validated --> Processing : start_processing
    Processing --> Compressing : compression_needed
    Processing --> Encrypting : skip_compression
    
    Compressing --> CompressionError : compression_failed
    Compressing --> Encrypting : compression_complete
    
    Encrypting --> EncryptionError : encryption_failed
    Encrypting --> Embedding : encryption_complete
    
    Embedding --> EmbeddingError : embedding_failed
    Embedding --> Finalizing : embedding_complete
    
    Finalizing --> ProcessingComplete : finalization_complete
    Finalizing --> ProcessingError : finalization_failed
    
    ProcessingComplete --> AwaitingDownload : file_ready
    AwaitingDownload --> Downloaded : file_downloaded
    AwaitingDownload --> Expired : timeout_reached
    
    %% Error states
    UploadError --> Idle : reset
    ValidationError --> Idle : reset
    CompressionError --> Idle : reset
    EncryptionError --> Idle : reset
    EmbeddingError --> Idle : reset
    ProcessingError --> Idle : reset
    
    %% Final states
    Downloaded --> [*]
    Expired --> [*]
    
    %% State descriptions
    Idle : Waiting for file upload
    Uploading : File transfer in progress
    ValidationPending : File uploaded, awaiting validation
    Validating : Checking file format and size
    Validated : File passed validation
    Processing : Starting processing pipeline
    Compressing : Applying compression algorithm
    Encrypting : Applying encryption
    Embedding : Hiding data in media
    Finalizing : Creating output file
    ProcessingComplete : Processing finished successfully
    AwaitingDownload : File ready for download
    Downloaded : File successfully downloaded
    Expired : File expired and cleaned up
```

### User Session State Machine

```mermaid
stateDiagram-v2
    [*] --> Anonymous
    
    Anonymous --> SigningIn : sign_in_attempt
    Anonymous --> SigningUp : sign_up_attempt
    
    SigningIn --> SignInError : invalid_credentials
    SigningIn --> Authenticated : credentials_valid
    
    SigningUp --> SignUpError : registration_failed
    SigningUp --> Authenticated : registration_successful
    
    Authenticated --> Active : session_established
    Active --> Processing : start_operation
    Active --> Idle : no_activity
    
    Processing --> Active : operation_complete
    Processing --> ProcessingError : operation_failed
    
    Idle --> Active : user_activity
    Idle --> SessionExpired : timeout_reached
    
    Active --> SigningOut : logout_request
    SigningOut --> Anonymous : logout_complete
    
    %% Error recovery
    SignInError --> Anonymous : retry_or_cancel
    SignUpError --> Anonymous : retry_or_cancel
    ProcessingError --> Active : error_handled
    
    %% Automatic transitions
    SessionExpired --> Anonymous : session_cleanup
    
    %% State descriptions
    Anonymous : No authentication
    SigningIn : Authentication in progress
    SigningUp : Registration in progress
    Authenticated : Valid credentials received
    Active : User actively using system
    Processing : Operation in progress
    Idle : Authenticated but inactive
    SigningOut : Logout in progress
    SessionExpired : Session timed out
```

### QR Code Processing State Machine

```mermaid
stateDiagram-v2
    [*] --> QRIdle
    
    QRIdle --> QRGenerating : generate_qr_request
    QRIdle --> QRDecrypting : decrypt_qr_request
    
    QRGenerating --> QRCompressing : start_compression
    QRGenerating --> QREncrypting : skip_compression
    
    QRCompressing --> QRCompressionError : compression_failed
    QRCompressing --> QREncrypting : compression_complete
    
    QREncrypting --> QREncryptionError : encryption_failed
    QREncrypting --> QRCodeCreation : encryption_complete
    
    QRCodeCreation --> QRCreationError : qr_creation_failed
    QRCodeCreation --> QRStyling : qr_created
    
    QRStyling --> QRStyleError : styling_failed
    QRStyling --> QRComplete : styling_complete
    
    QRDecrypting --> QRExtracting : start_extraction
    QRExtracting --> QRExtractionError : extraction_failed
    QRExtracting --> QRDecryptingData : data_extracted
    
    QRDecryptingData --> QRDecryptionError : decryption_failed
    QRDecryptingData --> QRDecompressing : decryption_complete
    
    QRDecompressing --> QRDecompressionError : decompression_failed
    QRDecompressing --> QRDecryptComplete : decompression_complete
    
    %% Success states
    QRComplete --> QRIdle : reset
    QRDecryptComplete --> QRIdle : reset
    
    %% Error recovery
    QRCompressionError --> QRIdle : reset
    QREncryptionError --> QRIdle : reset
    QRCreationError --> QRIdle : reset
    QRStyleError --> QRIdle : reset
    QRExtractionError --> QRIdle : reset
    QRDecryptionError --> QRIdle : reset
    QRDecompressionError --> QRIdle : reset
    
    %% State descriptions
    QRIdle : Ready for QR operations
    QRGenerating : Starting QR generation
    QRCompressing : Compressing message data
    QREncrypting : Encrypting compressed data
    QRCodeCreation : Creating QR code matrix
    QRStyling : Applying visual styling
    QRComplete : QR code generation complete
    QRDecrypting : Starting QR decryption
    QRExtracting : Extracting data from QR
    QRDecryptingData : Decrypting extracted data
    QRDecompressing : Decompressing decrypted data
    QRDecryptComplete : QR decryption complete
```

---

## Diagram Usage Guidelines

### Mermaid.js Syntax Notes
- All diagrams use proper Mermaid.js syntax compatible with GitHub and modern documentation platforms
- Relationship arrows follow Mermaid standards: `-->`, `-.->`, `==>`
- State diagrams use `stateDiagram-v2` for enhanced features
- Class diagrams use proper inheritance (`<|--`) and composition (`*--`) notation
- Sequence diagrams include proper participant definitions and message flows

### Customization Options
- Colors and styling can be applied using Mermaid themes
- Diagrams can be rendered in various formats (SVG, PNG, PDF)
- Interactive features available in supported platforms
- Responsive design for different screen sizes

### Integration
- All diagrams are designed to work together as a comprehensive system view
- Cross-references between diagrams maintain consistency
- Suitable for technical documentation, presentations, and system analysis 