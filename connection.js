//import mysql from 'mysql';

const mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "root",
  database:'hsclima'
});


getRegiao()

function getRegiao(){
    con.connect(function(err) {
    if (err) throw err;
    con.query("SELECT * FROM regiao", function (err, result, fields) {
        if (err) throw err;
        return result;
        });
    });
}