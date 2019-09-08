/*
CREATE USER 'username'@'localhost'
  IDENTIFIED BY 'password';
GRANT ALL
  ON nepc.*
  TO 'username'@'localhost';
*/
CREATE USER 'nepc'@'localhost'
  IDENTIFIED BY 'nepc';
GRANT SELECT
  ON nepc.* 
  TO 'nepc'@'localhost';
