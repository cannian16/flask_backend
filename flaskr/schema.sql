DROP TABLE IF EXISTS message;

-- 留言表
CREATE TABLE  message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    website_url TEXT,
    content TEXT NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address TEXT,
    user_agent TEXT
);
-- 友情链接表
CREATE TABLE  friendlink (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_name TEXT NOT NULL,
    favicon_url TEXT,
    `description` TEXT NOT NULL,
    site_url TEXT NOT NULL
);
