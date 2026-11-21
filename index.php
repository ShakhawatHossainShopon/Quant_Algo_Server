<?php
header('Content-Type: application/json');
echo json_encode([
    'status' => 'success',
    'message' => 'Quant Algo Server is running',
    'timestamp' => date('Y-m-d H:i:s')
]);
