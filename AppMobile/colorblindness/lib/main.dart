import 'dart:async';
import 'dart:io';
import 'package:gallery_saver/gallery_saver.dart';

import 'package:colorblindness/service/daltonize_service.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:progress_dialog/progress_dialog.dart';

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
  ProgressDialog progressDialog;

  bool processImage = false;
  int selectedItem = 1;

  _openGallary(BuildContext context) async {
    // ignore: deprecated_member_use
    File picture = await ImagePicker.pickImage(source: ImageSource.gallery);
    _processImage(picture, context);
  }

  _openCamera(BuildContext context) async {
    // ignore: deprecated_member_use
    File picture = await ImagePicker.pickImage(source: ImageSource.camera);
    _processImage(picture, context);
  }

  _processImage(File picture, BuildContext context) async {
    Navigator.of(context).pop(); // Fecha a caixa de dialogo
    await _uploadImage(picture);
  }

  _uploadImage(File picture) async {
    progressDialog.show();
    File file =
        await DaltonizeService.uploadImage(picture, processImage, selectedItem);
    setState(() {
      _image = file;
      progressDialog.hide();
    });
    //_saveImage();
  }

  _saveImage() {
    if (_image != null && _image.path != null) {
      GallerySaver.saveImage(_image.path);
    }
  }

  Future<void> _showChoiceDialog(BuildContext context) {
    return showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: Text("Ecolha:"),
            content: SingleChildScrollView(
              child: ListBody(
                children: <Widget>[
                  GestureDetector(
                    child: Text("Galeria"),
                    onTap: () {
                      _openGallary(context);
                    },
                  ),
                  Padding(
                    padding: EdgeInsets.all(8.0),
                  ),
                  GestureDetector(
                    child: Text("Câmera"),
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

  List<Widget> _decideDownloadButtonView() {
    if (_image == null) {
      return List<Widget>();
    } else {
      List<Widget> list = List<Widget>();
      list.add(IconButton(
        icon: Icon(Icons.file_download),
        onPressed: () {
          _saveImage();
        },
      ));
      return list;
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

  void _progressDialog(context) {
    progressDialog = new ProgressDialog(context);
    progressDialog.style(
        message: 'Processando ...',
        borderRadius: 10.0,
        backgroundColor: Colors.white,
        progressWidget: CircularProgressIndicator(),
        elevation: 10.0,
        insetAnimCurve: Curves.easeInOut,
        progress: 0.0,
        maxProgress: 100.0,
        progressTextStyle: TextStyle(
            color: Colors.black, fontSize: 13.0, fontWeight: FontWeight.w400),
        messageTextStyle: TextStyle(
            color: Colors.black, fontSize: 19.0, fontWeight: FontWeight.w600));
  }

  _appBar() {
    return AppBar(
      backgroundColor: Colors.grey[800],
      title: Text("Nome do APP"),
      actions: _decideDownloadButtonView(),
    );
  }

  @override
  Widget build(BuildContext context) {
    _progressDialog(context);

    return Scaffold(
      appBar: _appBar(),
      body: Container(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: <Widget>[_imageView(), _options(), _submitImage()],
          ),
        ),
      ),
    );
  }
}
