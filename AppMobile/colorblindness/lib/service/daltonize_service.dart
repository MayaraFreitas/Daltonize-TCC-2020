import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';

class DaltonizeService {
  static uploadImage(File _image, bool processImage, int _daltonismType) async {
    //var url = "http://127.0.0.1:5000/processImage";
    var url = "http://192.168.15.73:5000/processImage";

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

    //String basePath = (await getApplicationSupportDirectory()).path;
    String basePath = (await getTemporaryDirectory()).path;
    String dateTime = new DateTime.now().toString();
    print(dateTime);
    //File newFile = new File("${(await getTemporaryDirectory()).path}/image-$dateTime.jpg");
    File newFile = new File("$basePath/image-$dateTime.jpg");
    response.stream.listen((value) {
      newFile.writeAsBytes(value);
    });
    return newFile;
  }
}