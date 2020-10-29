import 'dart:async';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';

class DaltonizeService {
  static uploadImage(File _image, bool processImage, int _daltonismType) async {
    //var url = "http://127.0.0.1:5000/processImage";
    var url = "http://192.168.15.73:5000/processImage";
    var process = Completer();
    // This allows us to create (not send) a multipart POST request using
    // his req object has a member Map called fields for textual values and a List called files to which you can add MultipartFiles.
    var request = http.MultipartRequest('POST', Uri.parse(url));

    int type = processImage ? (3 + _daltonismType) : _daltonismType;
    request.fields['type'] = type.toString();

    var fileName = _image.path.split("/")?.last;
    var file = http.MultipartFile.fromBytes('file', _image.readAsBytesSync(),
        filename: fileName);

    request.files.add(file);

    var response = await request.send();

    String basePath = (await getTemporaryDirectory()).path;
    String dateTime = new DateTime.now().toString();
    String extension = _image.path.split(".")?.last;
    List<int> bytes = new List<int>();
    var newFile = new File("$basePath/image-$dateTime.$extension");

    // var subscription = response.stream.listen((value) => {bytes.addAll(value)},
    //     onError: (err) => print("error: $err"),
    //     onDone: () => {
    //       newFile.writeAsBytes(bytes)
    //       });

    var watch = response.stream.listen((value) async {
      print('------------>  AAAAAAAAAAAAAAA');
      bytes.addAll(value);
    });
    watch.onDone(() {
      print('------> onDone: ' + process.isCompleted.toString());
      if (!process.isCompleted) {
        newFile.writeAsBytes(bytes);
        process.complete('done');
      }
    });
    print('--------> awaiting.....');
    await process.future;
    print('------------> SAINDOO!!!');
    return newFile;
  }

  File _setBytes(File file, List<int> bytes) {
    file.writeAsBytes(bytes);
    return file;
  }
}
