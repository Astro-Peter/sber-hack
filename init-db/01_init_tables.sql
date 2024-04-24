CREATE TYPE topic_name AS ENUM ('ecology', 'it', 'other'); -- Дополните список по мере необходимости

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    name topic_name UNIQUE NOT NULL
);

CREATE TABLE topic_rates (
    id SERIAL PRIMARY KEY,
    topic_id INT NOT NULL,
    rating INT DEFAULT 0,
    month INT NOT NULL,
    year INT NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topics(id)
);


CREATE OR REPLACE FUNCTION add_topic_rating(topic_name topic_name, rating_increment INT, rating_date DATE) RETURNS VOID AS $$
DECLARE
    topic_id_to_update INT;
    v_year INT := EXTRACT(YEAR FROM rating_date);
    v_month INT := EXTRACT(MONTH FROM rating_date);
BEGIN
    -- Находим ID темы по её названию
    SELECT id INTO topic_id_to_update FROM topics WHERE name = topic_name;

    -- Проверяем, существует ли запись с данным годом и месяцем для данной темы
    IF NOT EXISTS (
        SELECT 1 FROM topic_rates WHERE topic_id = topic_id_to_update AND year = v_year AND month = v_month
    ) THEN
        -- Если записи нет, то создаем новую запись с начальным рейтингом
        INSERT INTO topic_rates (topic_id, rating, month, year) VALUES (topic_id_to_update, rating_increment, v_month, v_year);
    ELSE
        -- Если запись существует, обновляем рейтинг
        UPDATE topic_rates SET rating = rating + rating_increment WHERE topic_id = topic_id_to_update AND year = v_year AND month = v_month;
    END IF;
END;
$$ LANGUAGE plpgsql;