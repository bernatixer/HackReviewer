/**
 * Copyright (c) 2017-present, Viro, Inc.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree. An additional grant
 * of patent rights can be found in the PATENTS file in the same directory.
 */

import React, { Component } from 'react';

import {
  ViroARSceneNavigator
} from 'react-viro';

var sharedProps = {
  apiKey:"C86BB6B4-60CB-44E6-98AF-6949CBF5E1BE",
}

var WorldScene = require('./js/WorldScene');

var UNSET = "UNSET";
export default class ViroSample extends Component {
  constructor() {
    super();

    this.state = {
      sharedProps : sharedProps
    }
    this._exitViro = this._exitViro.bind(this);
  }

  render() {
    return (
      <ViroARSceneNavigator {...this.state.sharedProps}
        initialScene={{scene: WorldScene}} />
    );
  }


  // This function "exits" Viro by setting the navigatorType to UNSET.
  _exitViro() {
    this.setState({
      navigatorType : UNSET
    })
  }
}

module.exports = ViroSample
