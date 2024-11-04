const express = require('express');
const router = express.Router();
const taskController = require('../controllers/taskController');

router.post('/tasks', taskController.addTask);
router.get('/tasks', taskController.listTasks);
router.put('/tasks/:id', taskController.completeTask);

module.exports = router;
