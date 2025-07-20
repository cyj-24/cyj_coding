import React from 'react';
import { Card, List } from 'antd';

const AnalysisResult = ({ results }) => {
  if (!results || results.length === 0) return null;
  return (
    <Card title="分析结果" style={{ marginTop: 24 }}>
      <List
        dataSource={results}
        renderItem={(item, idx) => (
          <List.Item key={idx}>{item}</List.Item>
        )}
      />
    </Card>
  );
};

export default AnalysisResult;