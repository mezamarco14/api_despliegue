const { v4: uuidv4 } = require('uuid');
const client = require('../config/db');

exports.addTask = async (req, res) => {
    const { title } = req.body;
    const id = uuidv4();
    
    const query = 'INSERT INTO tasks (id, title, completed) VALUES (?, ?, ?)';
    await client.execute(query, [id, title, false], { prepare: true });
    res.status(201).json({ id, title, completed: false });
};

exports.listTasks = async (req, res) => {
    const query = 'SELECT id, title, completed FROM tasks';
    const result = await client.execute(query);
    res.json(result.rows);
};

exports.completeTask = async (req, res) => {
    const { id } = req.params;
    const query = 'UPDATE tasks SET completed = true WHERE id = ?';
    await client.execute(query, [id], { prepare: true });
    res.status(200).json({ message: `Tarea ${id} completada` });
};
