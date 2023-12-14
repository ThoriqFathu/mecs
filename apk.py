import streamlit as st

# import Stem

from cobastem import Stem
# import pandas as pd
import re
from streamlit_option_menu import option_menu

# from mecs import mecs as Stem


with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Stemming", "About"],
        default_index=0,
    )
# Judul halaman
if selected == "Stemming":
    st.title("mECS Stemmer for Madurese")
    # st.title("Aplikasi Stemming Bahasa Madura")
    # tag_hint = """
    #     <div style="background-color: #fdd271; width: 300px; padding: 10px;">
    #         <h5>Hint &#x1F4A1;</h5>
    #         <ul>
    #         <li>Writing ^a changes to â</li>
    #         <li>Writing `e changes to è</li>
    #         <li>Writing `d changes to ḍ</li>
    #         </ul>
    #         <p>Example:</p>
    #         <ul>
    #         <li>ab^a' &rarr; abâ'</li>
    #         <li>l`eker &rarr; lèker</li>
    #         <li>a`d`dhep &rarr; aḍḍhep</li>
    #         </ul>
    #     </div>
    # """

    tag_hint = """
        <div style="background-color: #fdd271; width: 500px; padding: 10px;">
            <h5>Hint &#x1F4A1;</h5>
            <p>Typing Madurese accented characters:</p>
            <div style="display: flex;">
                <div>
                    <table style="width:200px; text-align:center; margin:auto;">
                    <tr>
                        <td style="border: solid 1px black;">â</td>
                        <td style="border: solid 1px black;">^ + a</td>
                    </tr>
                    <tr>
                        <td style="border: solid 1px black;">è</td>
                        <td style="border: solid 1px black;">` + e</td>
                    </tr>
                    <tr>
                        <td style="border: solid 1px black;">ḍ</td>
                        <td style="border: solid 1px black;">. + d</td>
                    </tr>
                    <tr>
                        <td style="border: solid 1px black;">ṭ</td>
                        <td style="border: solid 1px black;">. + t</td>
                    </tr>
                    </table>
                </div>
                <div style="margin-left: 100px">
                <p>Example:</p>
                <ul>
                <li>ab^a' &rarr; abâ'</li>
                <li>l`eker &rarr; lèker</li>
                <li>a.d.dhep &rarr; aḍḍhep</li>
                <li>an.tok &rarr; anṭok</li>
                </ul>
            </div>
            </div>
            
        </div>
    """
    st.markdown(tag_hint, unsafe_allow_html=True)
    # with st.container() as container:
    st.markdown(
        "<p style='margin-bottom: -50px;'><strong>Input:</strong></p>",
        unsafe_allow_html=True,
    )
    # button_a = st.button("â")
    user_input = st.text_area("", placeholder="Write Madurese sentence")

    # st.text_area("", placeholder="Write the sentence" value = user_input+"â")
    # st.write("tru")

    # # Tampilkan hasil input
    # st.write("Anda memasukkan teks:", user_input)

    # # Tambahkan tombol
    if st.button("Stem"):
        # st.write(user_input)
        if user_input == "":
            st.warning("Empty input! Please input sentence!")
        else:
            pola = re.compile(r"\^a")
            user_input = re.sub(pola, "â", user_input)
            pola = re.compile(r"\`e")
            user_input = re.sub(pola, "è", user_input)
            pola = re.compile(r"\`d")
            user_input = re.sub(pola, "ḍ", user_input)
            pola = re.compile(r"\`t")
            user_input = re.sub(pola, "ṭ", user_input)
            st.markdown("<p><strong>Sentence:</strong></p>", unsafe_allow_html=True)
            st.write(user_input)
            stm = Stem.Stemmer()
            # user_input = 'Mènta tolong bâghiaghi sorat ka bapakna jupri'
            # user_input = stm.ghalluIdentification(user_input)
            # user_input = stm.ceIdentification(user_input)
            user_input = stm.cf(user_input)
            # print(user_input)
            user_input = stm.tokenizing(user_input)
            # st.write(user_input)
            # st.write(user_input)
            hasil = ""
            data = []
            dic_con = True
            # tag_data = "<table>"
            tag_data = "<table style='text-align: center;'><tr><th>Term</th><th>Lemma</th><th>Prefix</th><th>Suffix</th><th>Nasal</th></tr>"
            for i, kata in enumerate(user_input):
                stem = Stem.Stemmer()
                stem.stemming(kata)
                # data.append([kata, stem.lemma, stem.prefix, stem.suffix, stem.nasal])
                if stem.dic == True:
                    tag_data += f"""<tr>
                        <td>{kata}</td>
                        <td>{stem.lemma}</td>
                        <td>{stem.prefix}</td>
                        <td>{stem.suffix}</td>
                        <td>{stem.nasal}</td>
                    </tr>"""
                else:
                    dic_con = False
                    tag_data += f"""<tr style="background-color: pink;">
                        <td>{kata}</td>
                        <td>{stem.lemma}</td>
                        <td>{stem.prefix}</td>
                        <td>{stem.suffix}</td>
                        <td>{stem.nasal}</td>
                    </tr>"""
                # st.write(stem.lemma)
                hasil += stem.lemma + " "
            tag_data += "</table>"
            # df = pd.DataFrame(data, columns=["Term", "Lemma", "Prefix", "Suffix", "Nasal"])
            # d = "èkoa"
            # st.write(d.startswith("e"))
            st.markdown("<p><strong>Output:</strong></p>", unsafe_allow_html=True)
            # st.write("Output:")
            st.success(hasil)
            # st.write("Detail:")
            st.markdown("<p><strong>Detail:</strong></p>", unsafe_allow_html=True)
            # st.dataframe(df)
            st.markdown(tag_data, unsafe_allow_html=True)
            if not dic_con:
                st.markdown(
                    "<p style='padding-top: 10px;'><strong>Note:</strong></p>",
                    unsafe_allow_html=True,
                )
                tag_note = "<table style='text-align: center;'><tr><th>Color</th><th>Description</th></tr><tr><td style='background-color: pink;'></td><td>Lemma not in dictionary</td></tr></table>"
                st.markdown(tag_note, unsafe_allow_html=True)
            # st.dataframe(df, width=800)

    # st.markdown(
    #     f"""<div style='margin-top: 100px;'>
    #     <h3>References:</h3>
    #     <ul><li>F. H. Rachman, N. Ifada, S. Wahyuni, G. D. Ramadani and A. Pawitra, ModifiedECS (mECS) Algorithm for Madurese-Indonesian Rule-Based Machine Translation, In <i> Proceedings of The  2022 International Conference of Science and Information Technology in Smart Administration (ICSINTESA)</i>, Denpasar, Bali, Indonesia, 2022, pp. 51-56, IEEE, doi:<a href='https://doi.org/10.1109/ICSINTESA56431.2022.10041470'> 10.1109/ICSINTESA56431.2022.10041470</a></li></ul><div>""",
    #     unsafe_allow_html=True,
    # )

if selected == "About":
    st.title("About the Application")

    # Informasi tentang aplikasi atau proyek
    # st.write(
    #     "Selamat datang di Aplikasi Streamlit About. Aplikasi ini dibuat sebagai contoh sederhana "
    #     "menggunakan Streamlit untuk membuat halaman 'about'."
    # )

    # Informasi tentang penulis atau tim
    # st.header("Sekilas Aplikasi")
    # st.write(
    #     "Spelling correction adalah proses identifikasi dan perbaikan kesalahan ejaan dalam sebuah teks. Aplikasi spelling correction membantu pengguna untuk menemukan kata-kata yang salah eja dan menawarkan saran perbaikan. Aplikasi ini memiliki 2 fitur. Fitur pertama digunakan untuk spelling correction Bahasa Madura. Sedangkan fitur kedua digunakan untuk perhitungan kemiripan atau kedekatan antara dua kata. Pada fitur kedua juga menyertakan detil perhitungan dari setiap metode."
    # )
    st.header("Application Overview")
    st.write(
        """Stemming is the process of transforming a word’s form into a root word without considering the meaning of the deleted affix. In the Madurese language, an affix may have more than
one meaning or translation, depending on the attachment of the word in a sentence. This application using the Modified ECS (mECS) algorithm, which focuses on converting word forms into root words, managing the affixes, and synchronizing the results with Machine Translation. We implement the Rule-based concept to develop rules for the management of affixes. The application also includes detailed stemming results such as terms, lemmas, prefixes, suffixes, and nasals."""
    )

    # Kontak atau informasi lainnya
    # st.header("Metode Pada Aplikasi")

    # st.header("Method on Application")
    # st.markdown(
    #     """<div>
    #         This application applies 5 spelling correction methods, namely:
    #         <ul>
    #             <li>Hamming Distance</li>
    #             <li>Levenshtein Distance</li>
    #             <li>Damerau-Levenshtein Distance</li>
    #             <li>Jaro Similarity</li>
    #             <li>Jaro-Winkler Similarity</li>
    #         </ul>
    #     </div>""",
    #     unsafe_allow_html=True,
    # )
    st.header("Developer Team")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image("ibu_Ifada.jpg", caption="Noor Ifada", width=100)
    with col2:
        st.image("thoriq1.jpg", caption="Fika Hastarita Rachman", width=100)
    with col3:
        st.image("ibu_sri1.jpeg", caption="Sri Wahyuni", width=100)
    with col4:
        st.image("thoriq1.jpg", caption="Muhammad Fathuthoriq", width=100)
    with col5:
        st.image("thoriq1.jpg", caption="Moh. Amirullah", width=100)
    # st.markdown("""<img src="thoriq.jpg">""", unsafe_allow_html=True)
    st.header("Contact Us")
    st.markdown(
        f"""<div>
        <ul>
        <li>Noor Ifada : <a href='noor.ifada@trunojoyo.ac.id'>noor.ifada@trunojoyo.ac.id</a></li>
        <li>Fika Hastarita Rachman : <a href='example@trunojoyo.ac.id'>example@trunojoyo.ac.id</a></li>
        <li>Sri Wahyuni : <a href='example@trunojoyo.ac.id'>example@trunojoyo.ac.id</a></li>
        <li>Muhammad Fathuthoriq : <a href='thoriq771@gmail.com'>thoriq771@gmail.com</a></li>
        <li>Moh. Amirullah : <a href='example@trunojoyo.ac.id'>example@trunojoyo.ac.id</a></li>
        </ul><div>""",
        unsafe_allow_html=True,
    )
    st.header("References")
    st.markdown(
        f"""<div>
        <ul>
        <li>Rachman, F. H., Ifada, N., Wahyuni, S., Ramadani, G. D., & Pawitra, A. (2022, November). ModifiedECS (mECS) Algorithm for Madurese-Indonesian Rule-Based Machine Translation. In <i> Proceedings of The  2022 International Conference of Science and Information Technology in Smart Administration (ICSINTESA)</i> (pp. 51-56). IEEE. DOI: <a href='https://doi.org/10.1109/ICSINTESA56431.2022.10041470'>10.1109/ICSINTESA56431.2022.10041470</a></li>
        <li>Ifada, N., Rachman, F. H., Syauqy, M. W. M. A., Wahyuni, S., & Pawitra, A. (2023). MadureseSet: Madurese-Indonesian Dataset. <i> Data in Brief, 48,</i> 109035. DOI: <a href='https://doi.org/10.1016/j.dib.2023.109035'>10.1016/j.dib.2023.109035</a></li>
        </ul><div>""",
        unsafe_allow_html=True,
    )
