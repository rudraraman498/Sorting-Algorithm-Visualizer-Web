import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import { Box, Slider, Button, Typography } from '@mui/material';

// Connect to the Python backend
const socket = io('http://localhost:5000');

const SortingVisualizer = () => {
  const [array, setArray] = useState([]);
  const [colors, setColors] = useState([]);
  const canvasRef = useRef(null);
  const [algorithm,setAlgorithm] = useState("bubble")

  const algorithms = [
    {label:"Bubble Sort",id:"bubble"},
    {label: "Merge Sort", id: "merge"},
    {label: "Quick Sort", id: "quick"}
  ];

  // State for slider values
  const [size, setSize] = useState(20);
  const [minValue, setMinValue] = useState(0);
  const [maxValue, setMaxValue] = useState(100);
  const [speed, setSpeed] = useState(0.5);

  // Listen for updates from the server
  useEffect(() => {
    socket.on('update', (data) => {
      setArray(data.array);
      setColors(data.colors);
      drawData(data.array, data.colors);
    });
    socket.on('done', (data) => {
      alert(data.message);
    });
    socket.on("error", (data)=>{
      alert("An error occurred, retry again");
    });
    return () => {
      socket.off('update');
      socket.off('done');
    };
  }, []);

  // Generate a random array based on slider inputs
  const generateArray = () => {
    const newArr = Array.from({ length: size }, () =>
      Math.floor(Math.random() * (maxValue - minValue + 1)) + minValue
    );
    setArray(newArr);
    drawData(newArr, new Array(newArr.length).fill('red'));
  };

  // Tell the backend to start sorting
  const startSorting = () => {
    socket.emit('start_sort', { array, speed, algorithm });
  };

  const UpdateAlgoritm = (newAlgo) => {
    setAlgorithm(newAlgo);
    //console.log(algorithm)
  };

  // Draw the current array on the canvas
  const drawData = (data, colorArray) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;
    const barWidth = canvasWidth / (data.length + 1);
    const offset = 10;
    const spacing = 10;
    const maxVal = Math.max(...data);

    data.forEach((value, index) => {
      const barHeight = (value / maxVal) * (canvasHeight - 20);
      const x = index * barWidth + offset + spacing;
      const y = canvasHeight - barHeight;

      ctx.fillStyle = colorArray[index];
      ctx.fillRect(x, y, barWidth - spacing, barHeight);

      ctx.fillStyle = "orange";
      ctx.fillText(value, x, y - 5);
    });
  };

  return (
    <Box
      sx={{
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
      }}
    >
      <Typography variant="h4" sx={{ marginBottom: 2 }}>
        Sorting Algorithm Visualizer
      </Typography>

      {/* Buttons */}
      <Box sx={{ display: 'flex', gap: 2, marginBottom: 3 }}>
        <Button variant="contained" color="primary" onClick={generateArray}>
          Generate Random Array
        </Button>
        <Autocomplete
          disablePortal
          options={algorithms}
          onChange={(e,newAlgo) => UpdateAlgoritm(newAlgo.id)}
          sx={{ width: 300 }}
          renderInput={(params) => <TextField {...params} label="Algorithms" />}
/>
        <Button variant="contained" color="secondary" onClick={startSorting}>
          Start Sorting
        </Button>
      </Box>

      {/* Sliders in a Single Row */}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 3,
          marginBottom: 3,
          flexWrap: 'wrap', // Responsive handling for smaller screens
        }}
      >
        <Box sx={{ width: 150 }}>
          <Typography fontSize={14}>Size: {size}</Typography>
          <Slider
            value={size}
            min={3}
            max={30}
            step={1}
            onChange={(e, newValue) => setSize(newValue)}
            valueLabelDisplay="auto"
          />
        </Box>

        <Box sx={{ width: 150 }}>
          <Typography fontSize={14}>Min: {minValue}</Typography>
          <Slider
            value={minValue}
            min={0}
            max={50}
            step={1}
            onChange={(e, newValue) => setMinValue(newValue)}
            valueLabelDisplay="auto"
          />
        </Box>

        <Box sx={{ width: 150 }}>
          <Typography fontSize={14}>Max: {maxValue}</Typography>
          <Slider
            value={maxValue}
            min={50}
            max={200}
            step={1}
            onChange={(e, newValue) => setMaxValue(newValue)}
            valueLabelDisplay="auto"
          />
        </Box>

        <Box sx={{ width: 150 }}>
          <Typography fontSize={14}>Speed: {speed}s</Typography>
          <Slider
            value={speed}
            min={0.1}
            max={2}
            step={0.1}
            onChange={(e, newValue) => setSpeed(newValue)}
            valueLabelDisplay="auto"
          />
        </Box>
      </Box>

      {/* Canvas */}
      <canvas ref={canvasRef} width={900} height={450} style={{ background: 'black', borderRadius: 10 }}></canvas>
    </Box>
  );
};

export default SortingVisualizer;
