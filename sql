-- Sử dụng hoặc tạo cơ sở dữ liệu demGT
CREATE DATABASE IF NOT EXISTS demGT;
USE demGT;
-- Kiểm tra dữ liệu mới nhất
SELECT * FROM dem_xe ORDER BY times DESC LIMIT 10;

-- Tạo bảng dem_xe nếu chưa tồn tại

CREATE TABLE IF NOT EXISTS dem_xe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_xe TINYINT(1) NOT NULL DEFAULT 0 CHECK (data_xe IN (0, 1)), -- 1: Có xe, 0: Không có xe
    loai_xe VARCHAR(50) DEFAULT NULL, -- Loại xe nhận diện (ô tô, xe máy, xe tải, xe buýt,...)
    so_luong INT DEFAULT 0, -- Số lượng xe nhận diện, khởi tạo là 0
    times TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Thời gian nhận diện
);

-- Chèn dữ liệu khởi tạo (mặc định không có xe)
INSERT INTO dem_xe (data_xe, loai_xe, so_luong) 
VALUES 
    (0, NULL, 0);


