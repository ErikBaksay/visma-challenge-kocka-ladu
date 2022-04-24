export interface Response {
  status:    string;
  errmsg:     string;
  error:     string;
  message:    [
    {title: string,
    description: string,
    uploaded_time: string,
    images: [
        [
            string,
            string,
            number
        ]
    ]}
  ];
  status_code: number;
}

