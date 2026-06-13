CREATE TABLE IF NOT EXISTS notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    materia_id VARCHAR(50) NOT NULL,
    semestre VARCHAR(20) NOT NULL,
    nota DECIMAL(3,2) NOT NULL,
    UNIQUE(estudiante_id, materia_id, semestre)
);
