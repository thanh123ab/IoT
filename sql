-- Sử dụng cơ sở dữ liệu demGT
USE demGT;
-- Kiểm tra dữ liệu mới nhất
SELECT * FROM dem_xe ORDER BY times DESC LIMIT 10;

-- Tạo bảng dem_xe nếu chưa tồn tại
CREATE TABLE IF NOT EXISTS dem_xe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_xe TINYINT(1) NOT NULL CHECK (data_xe IN (0, 1)), -- 1: Có xe, 0: Không có xe
    times TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Thêm dữ liệu mẫu vào bảng dem_xe
INSERT INTO dem_xe (data_xe) 
VALUES 
    (0), (1), (0), (1), (0), (1), (0), (1), (0), (1), 
    (1), (0), (0), (1), (1), (0), (1), (0), (1), (1), 
    (0), (1), (1), (0), (0), (1), (1), (0), (1), (0), 
    (1), (1), (0), (0), (1), (1), (0), (1), (0), (1), 
    (0), (1), (1), (0), (1), (0), (1), (1), (0), (1);


