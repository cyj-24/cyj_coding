import React from 'react';
import { Upload, Button } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const ImageUploader = ({ onChange }) => {
  return (
    <Upload
      listType="picture"
      multiple
      accept="image/*"
      beforeUpload={() => false} // 阻止自动上传
      onChange={onChange}
    >
      <Button icon={<UploadOutlined />}>上传图片</Button>
    </Upload>
  );
};

export default ImageUploader;