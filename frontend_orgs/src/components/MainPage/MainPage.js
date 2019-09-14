import React, {Component} from "react";
import { Layout, Menu, Icon, Button, Table, Divider, Tag, Popconfirm } from 'antd';
import './MainPage.css'
import {BrowserView, MobileView} from "react-device-detect";
import api from "../../api/api";
import 'antd/dist/antd.css'

const { Header, Content, Footer } = Layout;

const columns = [
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
      title: 'operation',
      dataIndex: 'operation',
      render: (text, record) =>(
          <Popconfirm title="Sure to delete?" onConfirm={() => null}>
            <a>Delete</a>
          </Popconfirm>
        )
    },
  ];

export class MainPage extends Component {

    state = {
        users: []
      }
      componentDidMount() {
        api.get("/messages").then(response => response.data)
        .then((data) => {
          this.setState({ users: data })
          console.log(this.state.users)
         })
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
                                <Table rowKey="image" dataSource={this.state.users} columns={columns} />;
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


