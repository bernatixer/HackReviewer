import React from 'react';
import {
  Image,
  Platform,
  ScrollView,
  StyleSheet,
  View,
  Button,
  TextInput,
  Alert
} from 'react-native';

import * as ImagePicker from 'expo-image-picker';
import {AsyncStorage} from 'react-native';

export default function ReviewScreen() {
  const [value, onChangeText] = React.useState('Useless Placeholder');
  const [source, onChangeImage] = React.useState(require('../assets/images/robot-prod.png'));
  
  return (
    <View style={styles.container} onLayout={_onStartView}>
      <ScrollView
        style={styles.container}
        contentContainerStyle={styles.contentContainer}>
        <View style={styles.welcomeContainer}>
          <Image
            source={source}
            style={styles.welcomeImage}
          />
        </View>

        <View style={styles.getStartedContainer}>

          <Button
            title="UPLOAD A PHOTO"
            onPress={_onPressButton}
          />
          <TextInput
            multiline={true}
            numberOfLines={6}
            style={{ textAlign: "center",width: "100%", borderColor: 'navy', borderWidth: 1 }}
            onChangeText={text => onChangeText(text)}
            value={value}
          />
          
          <Button
            title="Press me"
            onPress={_onPressButton}
          />

        </View>

      </ScrollView>

    </View>
  );
}

async function _onStartView() {
  await AsyncStorage.setItem('image', require('../assets/images/robot-prod.png'));
}

async function _onPressButton() {
  // Alert.alert('VALUE', value)
  let result = await ImagePicker.launchCameraAsync({});
  onChangeImage(result)
  // await AsyncStorage.setItem('image', result);
}

ReviewScreen.navigationOptions = {
  header: null,
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  developmentModeText: {
    marginBottom: 20,
    color: 'rgba(0,0,0,0.4)',
    fontSize: 14,
    lineHeight: 19,
    textAlign: 'center',
  },
  contentContainer: {
    paddingTop: 30,
  },
  welcomeContainer: {
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 20,
  },
  welcomeImage: {
    width: 100,
    height: 80,
    resizeMode: 'contain',
    marginTop: 3,
    marginLeft: -10,
  },
  getStartedContainer: {
    alignItems: 'center',
    marginHorizontal: 50,
  },
  homeScreenFilename: {
    marginVertical: 7,
  },
  codeHighlightText: {
    color: 'rgba(96,100,109, 0.8)',
  },
  codeHighlightContainer: {
    backgroundColor: 'rgba(0,0,0,0.05)',
    borderRadius: 3,
    paddingHorizontal: 4,
  },
  getStartedText: {
    fontSize: 17,
    color: 'rgba(96,100,109, 1)',
    lineHeight: 24,
    textAlign: 'center',
  },
  tabBarInfoContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    ...Platform.select({
      ios: {
        shadowColor: 'black',
        shadowOffset: { width: 0, height: -3 },
        shadowOpacity: 0.1,
        shadowRadius: 3,
      },
      android: {
        elevation: 20,
      },
    }),
    alignItems: 'center',
    backgroundColor: '#fbfbfb',
    paddingVertical: 20,
  },
  tabBarInfoText: {
    fontSize: 17,
    color: 'rgba(96,100,109, 1)',
    textAlign: 'center',
  },
  navigationFilename: {
    marginTop: 5,
  },
  helpContainer: {
    marginTop: 15,
    alignItems: 'center',
  },
  helpLink: {
    paddingVertical: 15,
  },
  helpLinkText: {
    fontSize: 14,
    color: '#2e78b7',
  },
});
