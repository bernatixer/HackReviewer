import React, {Component} from "react";
import { Layout, Menu, Icon, Table, Tag, Popconfirm, Divider } from 'antd';
import './MainPage.css'
import {BrowserView} from "react-device-detect";
import api from "../../api/api";
import 'antd/dist/antd.css'

const { Header, Content, Footer } = Layout;



export class MainPage extends Component {

  state = {
    users: [],
  }
  componentDidMount() {
    api.get("/messages").then(response => response.data)
    .then((data) => {
      this.setState({ users: data })
      console.log(this.state.users)
     })
}

  handleDelete(key) {
    console.log(key);
    api.post("/messages/" + key + "/delete/" );
    api.get("/messages").then(response => response.data)
    .then((data) => {
      this.setState({ users: data })
    })
  };

  handleResolve(key) {
    console.log(key);
    api.post("/messages/" + key + "/resolve/" );
    api.get("/messages").then(response => response.data)
    .then((data) => {
      this.setState({ users: data })
    })
  };

  constructor(props){
    super(props);
    this.columns = [
      {
        title: 'Content',
        dataIndex: 'content',
        key: 'content',
      },
      {
        title: 'Language',
        dataIndex: 'language',
        key: 'language',
      },
      {
        title: 'Tags',
        dataIndex: 'tags',
        key: 'tags',
      },
      {
        title: 'Image Tags',
        dataIndex: 'image_tags',
        key: 'image_tags',
        render: image_tags => (
          <span>
            {image_tags.map(tag => {
              let color = tag.length > 5 ? "geekblue" : "green";
              return (
                <Tag color={color} key={tag}>
                  {tag.toUpperCase()}
                </Tag>
              );
            })}
          </span>
        )
      },
      {
        title: 'Image',
        dataIndex: 'image',
        key: 'image',
        render: image => image.length >= 1 ? (<img src={image} alt="test" width="100px" height="100px"/>) : null, 
      },
      {
        title: 'Status',
        dataIndex: 'resolved',
        key: 'resolved',
        render: resolved => resolved ? ("Resolved") : null,
        sorter: (a, b) => a.resolved != b.resolved,
        sortDirections: ['descend', 'ascend'],
      },
      {
        title: 'operation',
        dataIndex: 'operation',
        render: (text, record) =>(
          <span>
            <Popconfirm title="Sure to resolve?" onConfirm={() => this.handleResolve(record.id)}>
            <a>Resolve</a>
          </Popconfirm>
          <Divider type="vertical" />
          <Popconfirm title="Sure to delete?" onConfirm={() => this.handleDelete(record.id)}>
              <a>Delete</a>
          </Popconfirm>
          </span>
          )
      },
    ];
  }
    render() {
        return (
            <div>
                <BrowserView>
                    <Layout className="layout">
                        <Header className="header-style">
                            <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']} className="menu-style" >
                                <Menu.Item key="1" onClick={this.toHomePage}> <Icon type="home" /> Activity</Menu.Item>
                            </Menu>
                        </Header>
                        <Content className="content-style" >
                            <div className="components">
                                <h1>Hello World</h1>
                                <Table rowKey="image" dataSource={this.state.users} columns={this.columns} />;
                            </div>
                        </Content>
                        <Footer className="footer-style" >
                            Made with <Icon type="laptop" /> and <Icon type="heart" /> at HackTheNorth 2019
                        </Footer>
                    </Layout>
                </BrowserView>
            </div>
        )
    }
}


