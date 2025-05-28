 # System Architecture Documentation

This document provides comprehensive UML diagrams describing the steganography system architecture using Mermaid.js.

## 1. System Overview - Component Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Interface]
        CLI[Command Line Client]
        API_CLIENT[API Client]
    end
    
    subgraph "API Layer"
        FLASK[Flask API Server]
        AUTH[Authentication Middleware]
        ROUTES[API Routes]
    end
    
    subgraph "Core Services"
        CRYPTO[Encryption Service]
        STEGO[Steganography Service]
        COMPRESS[Compression Service]
        QR[QR Code Service]
    end
    
    subgraph "Utilities"
        UTILS[Utils Module]
        MEDIA[Media Processing]
        FILE[File Management]
    end
    
    subgraph "Storage"
        UPLOADS[Upload Directory]
        OUTPUT[Output Directory]
        STATIC[Static Assets]
    end
    
    %% Client connections
    WEB --> FLASK
    CLI --> FLASK
    API_CLIENT --> FLASK
    
    %% API Layer connections
    FLASK --> AUTH
    FLASK --> ROUTES
    AUTH --> ROUTES
    
    %% Service connections
    ROUTES --> CRYPTO
    ROUTES --> STEGO
    ROUTES --> COMPRESS
    ROUTES --> QR
    
    %% Utility connections
    CRYPTO --> UTILS
    STEGO --> UTILS
    COMPRESS --> UTILS
    QR --> UTILS
    UTILS --> MEDIA
    UTILS --> FILE
    
    %% Storage connections
    FILE --> UPLOADS
    FILE --> OUTPUT
    WEB --> STATIC
    
    %% Styling
    classDef clientLayer fill:#e1f5fe
    classDef apiLayer fill:#f3e5f5
    classDef serviceLayer fill:#e8f5e8
    classDef utilityLayer fill:#fff3e0
    classDef storageLayer fill:#fce4ec
    
    class WEB,CLI,API_CLIENT clientLayer
    class FLASK,AUTH,ROUTES apiLayer
    class CRYPTO,STEGO,COMPRESS,QR serviceLayer
    class UTILS,MEDIA,FILE utilityLayer
    class UPLOADS,OUTPUT,STATIC storageLayer
```

## 2. Class Diagram - Core Components

```mermaid
classDiagram
    class FlaskApp {
        +config: dict
        +secret_key: str
        +upload_folder: str
        +output_folder: str
        +run(host, port, debug)
        +create_directories()
    }

    class APIRoutes {
        +health_check()
        +encrypt()
        +decrypt()
        +generate_qr()
        +encrypt_qr()
        +decrypt_qr()
        +download_file()
        +get_capabilities()
    }

    class AuthMiddleware {
        +require_api_auth()
        +validate_token()
        +check_session()
    }

    class EncryptionService {
        +encrypt_message(message, password)
        +decrypt_message(data, password)
        +derive_key(password, salt)
        +generate_strong_password()
    }

    class CompressionService {
        +compress_data(data)
        +decompress_data(data)
        +get_compression_info(message)
    }

    class SteganographyService {
        +hide_data_in_image(input, output, data)
        +extract_data_from_image(path)
        +hide_data_in_audio(input, output, data)
        +extract_data_from_audio(path)
        +convert_and_hide_in_image(input, output, data)
    }

    class QRCodeService {
        +generate_qr_code(data, output)
        +hide_message_in_qr(message, password, output)
        +extract_message_from_qr(path, password)
    }

    class MediaProcessor {
        +convert_audio_to_wav(path)
        +find_or_download_ffmpeg()
        +process_image_format(path)
    }

    class FileManager {
        +secure_filename(filename)
        +save_file(file, path)
        +get_file_size(path)
        +cleanup_temp_files()
    }

    class Client {
        +encrypt_message(api_url, file_path, message, password)
        +decrypt_message(api_url, file_path, password)
        +download_file(url, filename)
        +check_api_health(api_url)
    }

    %% Relationships
    FlaskApp --> APIRoutes : contains
    FlaskApp --> AuthMiddleware : uses
    APIRoutes --> EncryptionService : uses
    APIRoutes --> CompressionService : uses
    APIRoutes --> SteganographyService : uses
    APIRoutes --> QRCodeService : uses
    SteganographyService --> MediaProcessor : uses
    APIRoutes --> FileManager : uses
    Client --> APIRoutes : calls
    EncryptionService --> CompressionService : uses
    QRCodeService --> EncryptionService : uses

```

## 3. Sequence Diagram - Encryption Process

```mermaid
sequenceDiagram
    participant C as Client
    participant API as Flask API
    participant Auth as Auth Middleware
    participant Comp as Compression Service
    participant Enc as Encryption Service
    participant Stego as Steganography Service
    participant FS as File System
    
    C->>+API: POST /api/encrypt (file, message, password)
    API->>+Auth: validate_request()
    Auth-->>-API: authorized
    
    API->>+FS: save_uploaded_file()
    FS-->>-API: file_path
    
    API->>+Comp: get_compression_info(message)
    Comp-->>-API: compression_stats
    
    API->>+Enc: encrypt_message(message, password)
    Enc->>+Comp: compress_data(message)
    Comp-->>-Enc: compressed_data
    Enc->>Enc: derive_key(password)
    Enc->>Enc: aes_encrypt(compressed_data)
    Enc-->>-API: encrypted_data
    
    API->>+Stego: hide_data_in_image(file_path, encrypted_data)
    Stego->>Stego: convert_to_suitable_format()
    Stego->>Stego: embed_using_lsb()
    Stego->>+FS: save_output_file()
    FS-->>-Stego: output_path
    Stego-->>-API: success
    
    API-->>-C: response(download_url, stats)
```

## 4. Sequence Diagram - Decryption Process

```mermaid
sequenceDiagram
    participant C as Client
    participant API as Flask API
    participant Auth as Auth Middleware
    participant Stego as Steganography Service
    participant Enc as Encryption Service
    participant Comp as Compression Service
    
    C->>+API: POST /api/decrypt (file, password?)
    API->>+Auth: validate_request()
    Auth-->>-API: authorized
    
    API->>+Stego: extract_data_from_image(file_path)
    Stego->>Stego: scan_lsb_bits()
    Stego->>Stego: find_terminator()
    Stego-->>-API: extracted_data
    
    API->>API: parse_embedded_password()
    
    alt Password found in file
        API->>API: use_embedded_password()
    else Password provided
        API->>API: use_provided_password()
    else No password
        API-->>C: error(no_password)
    end
    
    API->>+Enc: decrypt_message(extracted_data, password)
    Enc->>Enc: extract_salt_iv()
    Enc->>Enc: derive_key(password, salt)
    Enc->>Enc: aes_decrypt(ciphertext)
    Enc->>+Comp: decompress_data(decrypted_data)
    Comp-->>-Enc: original_message
    Enc-->>-API: decrypted_message
    
    API-->>-C: response(message, stats)
```

## 5. State Diagram - File Processing States

```mermaid
stateDiagram-v2
    [*] --> Uploaded : File Upload
    
    Uploaded --> Validating : Validate Format
    Validating --> Valid : Format OK
    Validating --> Invalid : Format Error
    Invalid --> [*] : Return Error
    
    Valid --> Converting : Need Conversion
    Valid --> Processing : Ready to Process
    Converting --> Processing : Conversion Complete
    Converting --> ConversionFailed : Conversion Error
    ConversionFailed --> [*] : Return Error
    
    Processing --> Encrypting : Encryption Mode
    Processing --> Extracting : Decryption Mode
    
    Encrypting --> Compressing : Compress Message
    Compressing --> AESEncryption : Apply AES
    AESEncryption --> Embedding : Embed in Media
    Embedding --> Saving : Save Output
    Saving --> Complete : Success
    
    Extracting --> Scanning : Scan LSB
    Scanning --> Found : Data Found
    Scanning --> NotFound : No Data
    NotFound --> [*] : Return Error
    Found --> Decrypting : Decrypt Data
    Decrypting --> Decompressing : Decompress
    Decompressing --> Complete : Success
    
    Complete --> [*] : Return Result
```

## 6. Activity Diagram - Compression Decision Flow

```mermaid
flowchart TD
    Start([Start: Message Input]) --> GetSize[Get Message Size]
    GetSize --> Compress[Apply zlib Compression]
    Compress --> Compare{Compressed Size < Original Size?}
    
    Compare -->|Yes| UseCompressed[Use Compressed Data]
    Compare -->|No| UseOriginal[Use Original Data + Marker]
    
    UseCompressed --> SetFlag[Set Compression Flag = True]
    UseOriginal --> ClearFlag[Set Compression Flag = False]
    
    SetFlag --> CalcRatio[Calculate Compression Ratio]
    ClearFlag --> ZeroRatio[Set Ratio = 0%]
    
    CalcRatio --> Encrypt[Proceed to Encryption]
    ZeroRatio --> Encrypt
    
    Encrypt --> AddMarker[Add Compression Marker to Encrypted Data]
    AddMarker --> End([End: Ready for Steganography])
```

## 7. Deployment Diagram

```mermaid
graph TB
    subgraph "Client Environment"
        Browser[Web Browser]
        CLIClient[CLI Client]
    end
    
    subgraph "Server Environment"
        subgraph "Application Server"
            Flask[Flask Application]
            API[API Endpoints]
            Auth[Authentication]
        end
        
        subgraph "Core Services"
            Utils[Utils Module]
            Crypto[Crypto Services]
            Stego[Steganography Engine]
        end
        
        subgraph "File System"
            Uploads[/uploads/]
            Output[/output/]
            Static[/static/]
            Templates[/templates/]
        end
        
        subgraph "Dependencies"
            PIL[Pillow/PIL]
            CV2[OpenCV]
            Crypto_Lib[PyCryptodome]
            QR_Lib[qrcode]
            FFmpeg[FFmpeg]
        end
    end
    
    %% Client connections
    Browser -.->|HTTPS/HTTP| Flask
    CLIClient -.->|HTTP API| Flask
    
    %% Internal connections
    Flask --> API
    API --> Auth
    API --> Utils
    Utils --> Crypto
    Utils --> Stego
    
    %% File system access
    Flask --> Uploads
    Flask --> Output
    Flask --> Static
    Flask --> Templates
    
    %% Dependency usage
    Stego --> PIL
    Stego --> CV2
    Crypto --> Crypto_Lib
    Utils --> QR_Lib
    Utils --> FFmpeg
    
    %% Styling
    classDef client fill:#e3f2fd
    classDef server fill:#f1f8e9
    classDef storage fill:#fff3e0
    classDef deps fill:#fce4ec
    
    class Browser,CLIClient client
    class Flask,API,Auth,Utils,Crypto,Stego server
    class Uploads,Output,Static,Templates storage
    class PIL,CV2,Crypto_Lib,QR_Lib,FFmpeg deps
```

## 8. Data Flow Diagram

```mermaid
flowchart LR
    subgraph "Input"
        UserFile[User File]
        Message[Secret Message]
        Password[Password]
    end
    
    subgraph "Processing Pipeline"
        Validate[Validate Input]
        Compress[Compress Message]
        Encrypt[Encrypt Data]
        Embed[Embed in Media]
    end
    
    subgraph "Output"
        StegoFile[Steganographic File]
        Stats[Compression Stats]
        DownloadLink[Download Link]
    end
    
    subgraph "Storage"
        TempStorage[(Temporary Storage)]
        OutputStorage[(Output Storage)]
    end
    
    %% Data flow
    UserFile --> Validate
    Message --> Compress
    Password --> Encrypt
    
    Validate --> TempStorage
    Compress --> Encrypt
    TempStorage --> Embed
    Encrypt --> Embed
    
    Embed --> OutputStorage
    OutputStorage --> StegoFile
    Compress --> Stats
    OutputStorage --> DownloadLink
    
    %% Styling
    classDef input fill:#e8f5e8
    classDef process fill:#e1f5fe
    classDef output fill:#fff3e0
    classDef storage fill:#fce4ec
    
    class UserFile,Message,Password input
    class Validate,Compress,Encrypt,Embed process
    class StegoFile,Stats,DownloadLink output
    class TempStorage,OutputStorage storage
```

## Architecture Summary

The steganography system follows a layered architecture with clear separation of concerns:

1. **Presentation Layer**: Web interface and CLI client
2. **API Layer**: Flask-based REST API with authentication
3. **Service Layer**: Core business logic (encryption, compression, steganography)
4. **Utility Layer**: Helper functions and media processing
5. **Storage Layer**: File management and temporary storage

Key design patterns implemented:
- **MVC Pattern**: Separation of routes, business logic, and data
- **Service Pattern**: Encapsulated business logic in service classes
- **Middleware Pattern**: Authentication and request processing
- **Factory Pattern**: Dynamic service instantiation based on media type
- **Strategy Pattern**: Different encryption strategies based on message size