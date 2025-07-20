import axios from 'axios';

// images: File[]
export const analyzeImages = async (images) => {
  const formData = new FormData();
  images.forEach((img) => formData.append('images', img));
  // 假设后端接口为 /api/analyze
  const res = await axios.post('/api/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
};