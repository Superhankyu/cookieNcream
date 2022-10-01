package com.example.myapplication.fragment

import android.app.Activity
import android.content.Context
import android.database.Cursor
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import androidx.navigation.Navigation
import androidx.navigation.fragment.navArgs
import com.example.myapplication.R
import kotlinx.android.synthetic.main.fragment_search.*
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import java.io.File
import java.io.IOException
import java.util.concurrent.TimeUnit
import android.provider.MediaStore
import androidx.loader.content.CursorLoader
import com.example.myapplication.MainActivity
import android.provider.DocumentsContract





// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"


/**
 * A simple [Fragment] subclass.
 * Use the [SearchFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class SearchFragment : Fragment() {
    // TODO: Rename and change types of parameters
    private var param1: String? = null
    private var param2: String? = null
    val args: SearchFragmentArgs by navArgs()

    //private var _binding : SearchFragment? = null
    //private val binding get() = _binding!!
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)



    }


    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view=inflater.inflate(R.layout.fragment_search, container, false)

        view.findViewById<Button>(R.id.Searchbutton_search).setOnClickListener{
            Navigation.findNavController(view).navigate(R.id.action_searchFragment_to_blankFragment)
        }

        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val path = args.path
        Log.d("TAG", path.toString())

        //val im = Uri.parse(path) // 공통 전처리 과정

        //var f = getRealPathFromURI(im) // 갤러리에서 온 경우
        //var a = im.path // 카메라에서 온 경우

        Log.d("real uri", path.toString())
        //Log.d("TAG!!!!", im.toString())
        var userimage: ImageView

        button222.setOnClickListener{ ///////////////// 이걸 누르면 사진이 서버로 전송됨.


            for(i in 0..5){

                val file1 = File(path.toString()) // 카메라에서 왔으면 im.path를 넣어야 하고 갤러리에서 왔으면 getRealpathfrom(im)을 넣어야한다.
                Log.d("thi s sdfiaodfjdsaoifja", path!!)
                //var bitmap = BitmapFactory.decodeResource(resources, R.drawable.mannish_33); // picture to send!!!!
                // 여기에 파일 경로를 넣으면됩니다!!!!!
                val file = File("/sdcard/Android/data/com.example.serverpractice/files/pictures", "img.jpg")
                //val outputStream = FileOutputStream(file);
                //bitmap.compress(Bitmap.CompressFormat.JPEG, 10, outputStream)
                //outputStream.close()

                //Log.d("thi s sdfiaodfjdsaoifja", a!!)
                val requestBody: RequestBody = MultipartBody.Builder()
                    .setType(MultipartBody.FORM)
                    .addFormDataPart(
                        "image", "img.jpg",
                        RequestBody.create("image/jpg".toMediaTypeOrNull(), file1)
                    )
                    .addFormDataPart("somParam", "someValue")
                    .build()

                /*if (file.exists()) {
                    println("i am here")
                } else {
                    println("not!!!!")
                }*/

                val url = "http://192.168.1.181:5000/"
                val client = OkHttpClient.Builder()
                    .connectTimeout(1000, TimeUnit.SECONDS)
                    .writeTimeout(1000, TimeUnit.SECONDS)
                    .readTimeout(1000, TimeUnit.SECONDS)
                    .build();


                val request = Request.Builder().url(url).header("Connection", "close").post(requestBody).build()

                client.newCall(request).enqueue(object : Callback {
                    override fun onFailure(call: Call, e: IOException) {
                        e.printStackTrace()
                        println("error!!!")
                    }

                    override fun onResponse(call: Call, response: Response) {
                        // val textView = findViewById<TextView>(R.id.textView)
                        println("???221")
                        val file = response.body?.byteStream()
                        println("???33321")
                        val bitmap = BitmapFactory.decodeStream(file)
                        println("???11")
                        val img = "imageView2"
                        var a = i+8

                        val resId = context?.resources?.getIdentifier("imageView$a","id",
                            context?.packageName
                        )


                        activity?.runOnUiThread {
                            userimage = view.findViewById(resId!!)
                            userimage.setImageBitmap(bitmap);
                        }


                    }
                })
            }


        }
    }

    private fun getRealPathFromURI1(contentUri: Uri): String? {
        val proj = arrayOf(MediaStore.Images.Media.DATA)
        val cursorLoader = CursorLoader(requireContext(), contentUri, proj, null, null, null)
        val cursor: Cursor? = cursorLoader.loadInBackground()
        val columnindex: Int = (cursor?.getColumnIndexOrThrow(MediaStore.Images.Media.DATA) ?: cursor?.moveToFirst()) as Int
        if (cursor != null) {
            cursor.moveToFirst();
            return cursor.getString(columnindex)
        }
        return "hi"
    }
    private fun getRealPathFromURI(contentUri: Uri): String? {
        if (contentUri.path!!.startsWith("/storage")) {
            return contentUri.path
        }
        val id = DocumentsContract.getDocumentId(contentUri).split(":").toTypedArray()[1]
        val columns = arrayOf(MediaStore.Files.FileColumns.DATA)
        val selection = MediaStore.Files.FileColumns._ID + " = " + id
        val cursor: Cursor? = activity?.contentResolver?.query(
            MediaStore.Files.getContentUri("external"),
            columns,
            selection,
            null,
            null
        )
        try {
            val columnIndex = cursor?.getColumnIndex(columns[0])
            if (cursor != null) {
                if (cursor.moveToFirst()) {
                    return columnIndex?.let { cursor.getString(it) }
                }
            }
        } finally {
            cursor?.close()
        }
        return null
    }


}