import React, { useState } from 'react';
import { Layout, Typography, message, Spin } from 'antd';
import ImageUploader from './ImageUploader';
import AnalysisResult from './AnalysisResult';
import { analyzeImages } from './api';
import 'antd/dist/reset.css';
import './App.css';

const { Header, Content } = Layout;
const { Title } = Typography;

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);

  const handleUploadChange = async (info) => {
    const files = info.fileList.map(f => f.originFileObj).filter(Boolean);
    if (files.length === 0) return;
    setLoading(true);
    setResults([]);
    try {
      const res = await analyzeImages(files);
      // 假设后端返回 { results: ["结论1", "结论2", ...] }
      setResults(res.results || []);
    } catch (err) {
      message.error('分析失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ background: '#fff', textAlign: 'center' }}>
        <Title level={2} style={{ margin: 0 }}>摇摆舞动作分析助手</Title>
      </Header>
      <Content style={{ padding: 24, maxWidth: 600, margin: '0 auto' }}>
        <ImageUploader onChange={handleUploadChange} />
        {loading ? <Spin style={{ marginTop: 24 }} /> : <AnalysisResult results={results} />}
      </Content>
    </Layout>
  );
}

export default App;
