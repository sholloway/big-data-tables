{ lib
, stdenv
, fetchzip
, makeWrapper
, coreutils
}:

let 
  pname = "spark";
  version = "3.3.1";
  sha512  = "sha512-c0g90BvoFB4bX7JmsrYYGBNlqLlFXMjRiIEjuS0le6wfIr0mRemu7vHky1wAiwvpFtFKejlWr7Fx/9Qrzn6C3g==";
                    
  # Create a variable that represents the untarred spark directory.
  untarDir = "${pname}-${version}";

in stdenv.mkDerivation {
  inherit pname version sha512 untarDir;

  # Download the spark tar file.
  src = fetchzip {
    url = "https://dlcdn.apache.org/spark/${pname}-${version}/${pname}-${version}-bin-hadoop3.tgz";
    sha512 = sha512;
  };
  nativeBuildInputs = [ makeWrapper ];
  buildInputs = [ ];

  # In the install phase take the following steps.
  # 1. Create directories:
  #       $out/lib/spark-3.3.1/conf
  #       $out/lib/spark-3.3.1/bin
  #       $out/lib/spark-3.3.1/share/java
  # 
  # 2. Copy the log4j properties file to ?..
  # 3. Create a spark-env.sh script that sets the environment variables for spark.
  # 4. Make a wrapper script for all the executables in $out/lib/spark-3.3.1/bin.
  # 5. Create sym links for all the spark jars to $out/share/java
  installPhase = ''
    mkdir -p $out/{lib/${untarDir}/conf,bin,/share/java}
    mv * $out/lib/${untarDir}

    cp $out/lib/${untarDir}/conf/log4j2.properties{.template,}

    cat > $out/lib/${untarDir}/conf/spark-env.sh <<- EOF
    export SPARK_HOME="$out/lib/${untarDir}"
    export PYSPARK_PYTHON="$out/bin/python"
    export PYTHONPATH="\$PYTHONPATH:$PYTHONPATH"
    EOF

    for n in $(find $out/lib/${untarDir}/bin -type f ! -name "*.*"); do
      makeWrapper "$n" "$out/bin/$(basename $n)"
      substituteInPlace "$n" --replace dirname ${coreutils.out}/bin/dirname
    done

    ln -s $out/lib/${untarDir}/lib/spark-assembly-*.jar $out/share/java
  '';
}