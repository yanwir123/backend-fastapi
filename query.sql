-- ===========================
-- CREATE TABLES
-- ===========================

-- Tabel users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT FALSE,
    otp_code VARCHAR(6),
    otp_expiry TIMESTAMP
);

-- Tabel uploads
CREATE TABLE uploads (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255),
    file_url TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel contact
CREATE TABLE contact (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel services
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel gallery
CREATE TABLE gallery (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel blog
CREATE TABLE blog (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ===========================
-- INSERT DUMMY DATA
-- ===========================

-- Dummy users
INSERT INTO users (username, email, password_hash, role, is_verified)
VALUES 
('yanuar', 'yanuar@example.com', 'hashpassword1', 'admin', TRUE),
('jane', 'jane@example.com', 'hashpassword2', 'user', FALSE),
('john', 'john@example.com', 'hashpassword3', 'user', TRUE);

-- Dummy uploads
INSERT INTO uploads (user_id, filename, file_url, status)
VALUES
(1, 'dokumen1.pdf', 'https://example.com/files/dokumen1.pdf', 'pending'),
(2, 'foto1.jpg', 'https://example.com/files/foto1.jpg', 'acc'),
(3, 'laporan.docx', 'https://example.com/files/laporan.docx', 'rejected');

-- Dummy contact
INSERT INTO contact (name, email, message)
VALUES
('Alice', 'alice@example.com', 'Halo, saya ingin bertanya.'),
('Bob', 'bob@example.com', 'Apakah layanan Anda tersedia di Jakarta?');

-- Dummy services
INSERT INTO services (title, description, image_url)
VALUES
('Jasa Desain', 'Kami menyediakan jasa desain grafis profesional.', 'https://example.com/images/service1.jpg'),
('Jasa Pembuatan Website', 'Membuat website modern dan responsive.', 'https://example.com/images/service2.jpg');

-- Dummy gallery
INSERT INTO gallery (title, image_url)
VALUES
('Proyek A', 'https://example.com/images/gallery1.jpg'),
('Proyek B', 'https://example.com/images/gallery2.jpg');

-- Dummy blog
INSERT INTO blog (title, content, image_url)
VALUES
('Tips Desain UI/UX', 'Konten blog tentang desain UI/UX.', 'https://example.com/images/blog1.jpg'),
('Cara Membuat Website Cepat', 'Konten blog tentang optimasi website.', 'https://example.com/images/blog2.jpg');
