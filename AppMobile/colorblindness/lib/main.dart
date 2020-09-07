import 'dart:async';
import 'dart:io';
import 'package:gallery_saver/gallery_saver.dart';

import 'package:colorblindness/service/daltonize_service.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

void main() {
  runApp(new MaterialApp(
    title: "Camera App",
    home: LandingScreen(),
  ));
}

class LandingScreen extends StatefulWidget {
  @override
  _LandingScreenState createState() => _LandingScreenState();
}

class _LandingScreenState extends State<LandingScreen> {
  File _image;

  bool processImage = false;
  int selectedItem = 1;

  _openGallary(BuildContext context) async {
    // ignore: deprecated_member_use
    File picture = await ImagePicker.pickImage(source: ImageSource.gallery);
    await _uploadImage(picture);
    Navigator.of(context).pop(); // Fecha a caixa de dialogo
  }

  _openCamera(BuildContext context) async {
    // ignore: deprecated_member_use
    File picture = await ImagePicker.pickImage(source: ImageSource.camera);
    await _uploadImage(picture);
    Navigator.of(context).pop(); // Fecha a caixa de dialogo
  }

  _uploadImage(File picture) async {
    File file =
        await DaltonizeService.uploadImage(picture, processImage, selectedItem);
    setState(() {
      _image = file;
    });
    //_saveImage();
  }

  _saveImage() async {
    if (_image != null && _image.path != null) {
      GallerySaver.saveImage(_image.path);
    }
  }

  Future<void> _showChoiceDialog(BuildContext context) {
    return showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text("Make a choice!"),
            content: SingleChildScrollView(
              child: ListBody(
                children: <Widget>[
                  GestureDetector(
                    child: Text("Gallary"),
                    onTap: () {
                      _openGallary(context);
                    },
                  ),
                  Padding(
                    padding: EdgeInsets.all(8.0),
                  ),
                  GestureDetector(
                    child: Text("Camera"),
                    onTap: () {
                      _openCamera(context);
                    },
                  )
                ],
              ),
            ),
          );
        });
  }

  _imageView() {
    return SizedBox(
      height: 300,
      child: _decideImageView(),
    );
  }

  Widget _decideImageView() {
    if (_image == null) {
      return Text("No Image Selected!");
    } else {
      return Image.file(
        _image,
        width: 300,
        height: 300,
      );
    }
  }

  String _getActionText() {
    return processImage ? "Melhorar Imagem" : "Simular Daltonismo";
  }

  Widget _switchButton() {
    return Column(children: [
      Switch(
        value: processImage,
        onChanged: (value) {
          setState(() {
            processImage = value;
          });
        },
        activeColor: Colors.black,
      ),
      Text(_getActionText()),
    ]);
  }

  Widget _dropDown() {
    return new DropdownButton(
        value: selectedItem,
        items: [
          DropdownMenuItem(
            child: Text("Protanopes"),
            value: 1,
          ),
          DropdownMenuItem(
            child: Text("Deuteranopes"),
            value: 2,
          ),
          DropdownMenuItem(
            child: Text("Tritanope"),
            value: 3,
          ),
        ],
        onChanged: (value) {
          setState(() {
            selectedItem = value;
          });
        });
  }

  Widget _options() {
    return Row(
      children: [
        Spacer(),
        _switchButton(),
        Spacer(),
        _dropDown(),
        Spacer(),
      ],
    );
  }

  Widget _submitImage() {
    return RaisedButton(
      onPressed: () {
        _showChoiceDialog(context);
      },
      child: Text("Selecione a Imagem"),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Nome do APP"),
      ),
      body: Container(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: <Widget>[
              _imageView(),
              _options(),
              _submitImage()
              // _switchButton(),
              // _dropDown()
              // Row(
              //   children: [_switchButton(), _dropDown()],
              // )
            ],
          ),
        ),
      ),
    );
  }

  // @override
  // Widget build(BuildContext context) {
  //   return Scaffold(
  //     appBar: AppBar(
  //       title: Text("Main Screen"),
  //     ),
  //     body: Container(
  //       child: Center(
  //         child: Column(
  //           mainAxisAlignment: MainAxisAlignment.spaceAround,
  //           children: <Widget>[
  //             _decideImageView(),
  //             _dropDown(),
  //             RaisedButton(
  //               onPressed: () {
  //                 _showChoiceDialog(context);
  //               },
  //               child: Text("Select Image"),
  //             )
  //           ],
  //         ),
  //       ),
  //     ),
  //   );
  // }
}
